import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.scrapper.driver import driver


def get_radicados_data():
    # Abrir una página
    url = "https://consultaprocesos.ramajudicial.gov.co/Procesos/NumeroRadicacion"
    driver.get(url)

    # Esperar que los radio buttons sean visibles
    wait = WebDriverWait(driver, 10)
    # Encontrar todos los radio buttons
    radio_buttons = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//input[@role='radio']")))

    # Seleccionar el segundo radio button con JavaScript
    if len(radio_buttons) > 1:
        driver.execute_script("arguments[0].click();", radio_buttons[1])
        print("✅ Segundo radio button seleccionado correctamente.")
    else:
        print("❌ No se encontraron suficientes radio buttons.")

    # Esperar el campo de entrada por su placeholder
    input_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Ingrese los 23 dígitos del número de Radicación']")))

    # Asignar el número de radicación
    numero_radicacion = "05001233300020210212000"  # Ingresa aquí el número que desees
    input_field.send_keys(numero_radicacion)
    print("✅ Número de radicación ingresado correctamente.")

    # Esperar el botón de "Consultar" y hacer clic
    consultar_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Consultar Número de radicación']")))
    consultar_button.click()
    print("✅ Botón 'Consultar' clickeado correctamente.")

    # Esperar a que la tabla cargue
    tabla = wait.until(EC.presence_of_element_located((By.XPATH, "//th[@aria-label='Fecha de Radicación y última actuación']/ancestor::table")))

    # Obtener todas las filas de la tabla
    filas = tabla.find_elements(By.XPATH, ".//tbody/tr")

    fechas = []
    despachos = []
    sujetos_columna = []

    # Recorrer cada fila para extraer la fecha
    for fila in filas:
        try:
            # Buscar el `td` correspondiente a la columna
            columna_fecha = fila.find_element(By.XPATH, ".//td[@class='text-center']")
            # Buscar el segundo botón dentro de la fila
            boton = columna_fecha.find_element(By.XPATH, "following-sibling::td//button")
            # Extraer el span dentro del botón (contiene la fecha)
            fecha = boton.find_element(By.XPATH, ".//span").text
            fechas.append(fecha)

            # Buscar el `td` siguiente al que contiene el botón
            despacho_columna = boton.find_element(By.XPATH, "ancestor::td/following-sibling::td")
            despacho = despacho_columna.find_element(By.XPATH, ".//div").text
            despachos.append(despacho)
            
            # Buscar el `td` siguiente al que contiene el despacho
            sujeto_columna = despacho_columna.find_element(By.XPATH, "following-sibling::td")
            sujeto = sujeto_columna.find_element(By.XPATH, ".//div").text
            sujetos_columna.append(sujeto)
        except Exception as e:
            print(f"⚠️ Error extrayendo fecha en una fila: {e}")

    # Imprimir los resultados
    print("📅 Fechas encontradas en la columna:")
    for fecha in fechas:
        print(f" - {fecha}")

    print("🏛️ Despachos encontrados en la columna:")
    for despacho in despachos:
        print(f" - {despacho}")

    print("👥 Sujetos encontrados en la columna:")
    for sujeto in sujetos_columna:
        print(f" - {sujeto}")

    # Cerrar el navegador
    driver.quit()