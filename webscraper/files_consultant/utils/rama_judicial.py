import re
import time
from dataclasses import dataclass

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from files_consultant.utils.driver import driver


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
    radio_buttons = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//input[@role='radio']")))

    if len(radio_buttons) > 1:
        driver.execute_script("arguments[0].click();", radio_buttons[1])
        print("✅ Second radio button selected successfully.")
    else:
        raise Exception("Not enough radio buttons found.")

    input_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Ingrese los 23 dígitos del número de Radicación']")))

    radicado_data_list = []

    for index, radicado_number in enumerate(radicado_numbers):
        print(f"🔍 Searching for radicado number {radicado_number}...")

        input_field.clear()
        input_field.send_keys(radicado_number)
        print(f"✅ Radicado number {radicado_number} entered successfully.")

        consult_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Consultar Número de radicación']")))
        driver.execute_script("arguments[0].scrollIntoView(true);", consult_button)
        # Add a small delay to ensure the page has settled
        time.sleep(0.5)
        # Try JavaScript click if regular click fails
        try:
            consult_button.click()
        except:
            driver.execute_script("arguments[0].click();", consult_button)
        print("✅ 'Consult' button clicked successfully.")

        table = wait.until(EC.presence_of_element_located((By.XPATH, "//th[@aria-label='Fecha de Radicación y última actuación']/ancestor::table")))

        try:
            row = table.find_element(By.XPATH, ".//tbody/tr[1]")

            date_column = row.find_element(By.XPATH, ".//td[@class='text-center']")
            open_date = date_column.find_element(By.XPATH, "following-sibling::td//div").text

            button = date_column.find_element(By.XPATH, "following-sibling::td//button")
            last_update_date = button.find_element(By.XPATH, ".//span").text

            office_column = button.find_element(By.XPATH, "ancestor::td/following-sibling::td")
            office = office_column.find_element(By.XPATH, ".//div").text

            legal_parties_column = office_column.find_element(By.XPATH, "following-sibling::td")
            legal_parties = legal_parties_column.find_element(By.XPATH, ".//div").text

            radicado_data_list.append(RadicadoData(open_date, last_update_date, office, legal_parties))
        except Exception as e:
            print(f"⚠️ Error extracting data for radicado number {radicado_number}: {e}")

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
