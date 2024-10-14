from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from datetime import datetime, timedelta

# Obtener la ruta de la carpeta Descargas por defecto
download_dir = os.path.join(os.path.expanduser('~'), 'Downloads')

chrome_options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": download_dir,  # Descargar en la carpeta Descargas por defecto
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True,
    "profile.default_content_settings.popups": 0,
    "profile.content_settings.exceptions.automatic_downloads.*.setting": 1
}
chrome_options.add_experimental_option("prefs", prefs)

# Configurar el navegador (asegúrate de tener el driver de Chrome instalado)
driver = webdriver.Chrome(options=chrome_options)

# URL de la página de inicio de sesión
login_url = 'https://s1.philaxmed.cl/Collecting.html#_'

# Abrir la página de inicio de sesión
driver.get(login_url)

# Esperar a que los campos de entrada estén presentes
rut_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Ej. 12345678-9"]')))
password_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'gwt-PasswordTextBox')))
login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "philaxButton-button") and .//i[contains(@class, "fa-sign-in-alt")]]')))

# Ingresar las credenciales
rut_input.send_keys('20083974-9')
password_input.send_keys('Javier12%')

# Usar JavaScript para hacer clic en el botón de inicio de sesión
driver.execute_script("arguments[0].click();", login_button)

# Esperar 10 segundos para que la página siguiente se cargue completamente
time.sleep(10)

# Espera a que el botón "Reportes" sea clickeable y haz clic en él
reportes_button = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, '//div[contains(@class, "topMenuItem-optionPanel")]//div[contains(text(), "Reportes")]/following-sibling::div[contains(@class, "expandable")]'))
)
reportes_button.click()

# Espera a que el submenú "Items Cobrados" sea visible
items_cobrados_button = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "topMenuItem-subMenu")]//div[contains(@class, "topMenuItem-optionPanel")]//div[contains(text(), "Items Cobrados")]/following-sibling::div[contains(@class, "topMenuItem-button")]'))
)

# Usar JavaScript para hacer clic en el botón "Items Cobrados"
driver.execute_script("arguments[0].click();", items_cobrados_button)

# Esperar unos segundos para asegurarse de que la acción se complete
time.sleep(5)

# Función para borrar y escribir la fecha en el formato correcto
def set_date(input_xpath, date):
    # Cerrar cualquier popup que pueda estar bloqueando
    try:
        popup = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'glassPopup')))
        driver.execute_script("arguments[0].style.display='none';", popup)
    except:
        pass  # Si no hay popup, continúa

    date_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, input_xpath)))
    date_input.click()
    for _ in range(10):
        date_input.send_keys('\ue003') 
    for char in date:
        date_input.send_keys(char)
        time.sleep(0.1)

# Fecha inicial y fecha final del rango deseado
start_date = datetime(2015, 1, 1)
end_date = datetime(2024, 9, 27)

while start_date < end_date:
    # Fecha actual y fecha después de 300 días desde la fecha inicial
    current_date = start_date.strftime('%d%m%Y')
    
    # Si la siguiente fecha futura es mayor que end_date, establecer future_date como end_date
    if start_date + timedelta(days=300) > end_date:
        future_date = end_date.strftime('%d%m%Y')
    else:
        future_date = (start_date + timedelta(days=300)).strftime('%d%m%Y')
    
    # Establecer la fecha futura en el campo "Hasta"
    set_date('//div[@class="inputWidget timeIntervalSearcher-endDateWidget"]//input[@class="gwt-TextBox filterDateTextBox calendarTextBox inputWidget-input inputEnabled"]', future_date)

    # Establecer la fecha inicial en el campo "Desde"
    set_date('//div[@class="inputWidget timeIntervalSearcher-startDateWidget"]//input[@class="gwt-TextBox filterDateTextBox calendarTextBox inputWidget-input inputEnabled"]', current_date)
    
    # Presionar el botón de búsqueda y esperar 10 segundos
    search_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//div[contains(@class, "billItemsView-searchButton")]//button[contains(@class, "gwt-Button philaxButtonColor-default philaxButton-button") and .//i[contains(@class, "fa-search")]]'))
    )
    search_button.click()
    
    # Esperar 10 segundos para que la búsqueda se complete
    time.sleep(120)
    
    # Espera a que el botón de descarga de Excel sea clickeable y haz clic en él
    excel_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "gwt-Button philaxButtonColor-default philaxButton-button") and .//i[contains(@class, "fa-file-excel")]]'))
    )
    excel_button.click()
    
    # Esperar unos segundos para asegurarse de que la acción se complete
    time.sleep(30)
    
    # Incrementar la fecha inicial en 300 días para el siguiente ciclo
    start_date += timedelta(days=300)

# Cerrar el navegador al finalizar todos los ciclos
driver.quit()
