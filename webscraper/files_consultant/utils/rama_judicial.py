import re
import time
from datetime import datetime
from dataclasses import dataclass

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from files_consultant.utils.driver import driver
from files_consultant import models as files_consultant_models


@dataclass
class RadicadoData:
    def __init__(self, open_date, last_update_date, office, legal_parties_str):
        self.open_date = open_date
        self.last_update_date = last_update_date
        self.office = office
        self.legal_parties_str = legal_parties_str

    def __str__(self):
        return f"Open Date: {self.open_date}\nLast Update Date: {self.last_update_date}\nOffice: {self.office}\nLegal Parties: {self.legal_parties_str}"


@dataclass
class LegalParties:
    plaintiff: str
    defendant: str
    procurator: str

    def __str__(self):
        return f"Plaintiff: {self.plaintiff}\nDefendant: {self.defendant}\nProcurator: {self.procurator}"


def get_radicado_data(radicado_numbers: list[str]) -> list[RadicadoData]:
    url = "https://consultaprocesos.ramajudicial.gov.co/Procesos/NumeroRadicacion"
    driver.get(url)

    wait = WebDriverWait(driver, 10)
    radio_buttons = wait.until(EC.presence_of_all_elements_located(
        (By.XPATH, "//input[@role='radio']")))

    if len(radio_buttons) > 1:
        driver.execute_script("arguments[0].click();", radio_buttons[1])
        print("✅ Second radio button selected successfully.")
    else:
        raise Exception("Not enough radio buttons found.")

    input_field = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@placeholder='Ingrese los 23 dígitos del número de Radicación']")))

    radicado_data_list = []

    for radicado_number in radicado_numbers:
        print(f"🔍 Searching for radicado number {radicado_number}...")

        input_field.clear()
        input_field.send_keys(radicado_number)
        print(f"✅ Radicado number {radicado_number} entered successfully.")

        consult_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[@aria-label='Consultar Número de radicación']")))
        driver.execute_script(
            "arguments[0].scrollIntoView(true);", consult_button)
        # Add a small delay to ensure the page has settled
        time.sleep(0.5)
        # Try JavaScript click if regular click fails
        try:
            consult_button.click()
        except:
            driver.execute_script("arguments[0].click();", consult_button)
        print("✅ 'Consult' button clicked successfully.")

        table = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//th[@aria-label='Fecha de Radicación y última actuación']/ancestor::table")))
        filas = table.find_elements(By.XPATH, ".//tbody/tr")

        fechas_apertura = []
        fechas = []
        despachos = []
        sujetos_columna = []

        for fila in filas:
            try:
                # Buscar el `td` correspondiente a la columna
                columna_fecha = fila.find_element(
                    By.XPATH, ".//td[@class='text-center']")

                # Extraer la fecha de apertura
                fecha_apertura = columna_fecha.find_element(
                    By.XPATH, "following-sibling::td//div").text
                fechas_apertura.append(fecha_apertura.split("\n")[0])

                # Buscar el segundo botón dentro de la fila
                boton = columna_fecha.find_element(
                    By.XPATH, "following-sibling::td//button")
                # Extraer el span dentro del botón (contiene la fecha)
                fecha = boton.find_element(By.XPATH, ".//span").text
                fechas.append(fecha)

                # Buscar el `td` siguiente al que contiene el botón
                despacho_columna = boton.find_element(
                    By.XPATH, "ancestor::td/following-sibling::td")
                despacho = despacho_columna.find_element(
                    By.XPATH, ".//div").text
                despachos.append(despacho)

                # Buscar el `td` siguiente al que contiene el despacho
                sujeto_columna = despacho_columna.find_element(
                    By.XPATH, "following-sibling::td")
                sujeto = sujeto_columna.find_element(By.XPATH, ".//div").text
                sujetos_columna.append(sujeto)
            except Exception as e:
                print(f"⚠️ Error extrayendo fecha en una fila: {e}")

        radicado_data_list.append(RadicadoData(
            open_date=fechas_apertura[0],
            last_update_date=fechas[0],
            office=despachos[0],
            legal_parties_str=sujetos_columna[0]
        ))

    return radicado_data_list


def extract_legal_parties(texto: str) -> LegalParties:
    """
    Extrae los involucrados de un texto con formato 'Rol: Nombre' y los retorna en una clase.

    Args:
        texto (str): Texto con los involucrados.

    Returns:
        Involucrados: Objeto con los datos estructurados.
    """
    pattern = r"([^:\n]+):\s*(.+)"
    matches = dict(re.findall(pattern, texto))

    return LegalParties(
        plaintiff=matches.get("Demandante", None),
        defendant=matches.get("Demandado", None),
        procurator=matches.get("Procurador", None)
    )


def process_radicados_from_shell(radicado_list: list[str]) -> None:
    """
    Process a list of radicado numbers from Django shell.
    Usage from Django shell:

    from files_consultant.utils.rama_judicial import process_radicados_from_shell
    radicados = ['23001233300020190025100', '23001233300020190025200']
    process_radicados_from_shell(radicados)
    """

    try:
        # Get data for all radicados
        results = get_radicado_data(radicado_list)

        for radicado_number, result in zip(radicado_list, results):
            if result:
                # Create or update Process
                process, created = files_consultant_models.Process.objects.get_or_create(
                    file_number=radicado_number
                )

                # Update process data
                process.open_date = datetime.strptime(
                    result.open_date, '%Y-%m-%d').date()

                # Extract legal parties
                parties = extract_legal_parties(result.legal_parties_str)
                process.plaintiff = parties.plaintiff.title() if parties.plaintiff else None
                process.defendant = parties.defendant.title() if parties.defendant else None
                process.procurator = parties.procurator.title() if parties.procurator else None

                process.save()
                print(
                    f"✅ {'Created' if created else 'Updated'} process: {radicado_number}")

                # Create snapshot
                files_consultant_models.ProcessSnapshot.objects.create(
                    process=process,
                    last_update=datetime.strptime(
                        result.last_update_date, '%Y-%m-%d')
                )
                print(f"✅ Created snapshot for: {radicado_number}")
            else:
                print(f"⚠️ No data found for: {radicado_number}")

    except Exception as e:
        print(f"❌ Error processing radicados: {str(e)}")
    finally:
        try:
            driver.delete_all_cookies()
            driver.get("about:blank")
        except:
            pass
