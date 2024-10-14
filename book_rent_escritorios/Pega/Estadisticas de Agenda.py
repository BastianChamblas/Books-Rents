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
login_url = 'https://s1.philaxmed.cl/Statistics.html#_'

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

# Esperar a que el botón "Estadísticas de Agenda" esté presente y hacer clic en él
agenda_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[contains(text(), "Estadísticas de Agenda")]/preceding-sibling::button')))
driver.execute_script("arguments[0].click();", agenda_button)

# Esperar unos segundos para que la acción se complete
time.sleep(5)

# Hacer clic en el elemento "Citas en el Tiempo"
citas_tiempo_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[contains(text(), "Citas en el Tiempo")]')))
driver.execute_script("arguments[0].click();", citas_tiempo_button)

# Esperar unos segundos para que la acción se complete
time.sleep(5)

# Función para borrar y escribir la fecha en el formato correcto
def set_date(input_xpath, date):
    date_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, input_xpath)))
    date_input.click()
    for _ in range(10):  # Asumimos que la fecha tiene un máximo de 10 caracteres incluyendo los guiones
        date_input.send_keys('\ue003') 
    for char in date:
        date_input.send_keys(char)
        time.sleep(0.1)  # Pequeña pausa para permitir que el formato se aplique

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
    
    # Establecer la fecha inicial en el campo "Desde"
    set_date('//div[@class="inputWidget timeIntervalSearcher-startDateWidget"]//input[@class="gwt-TextBox filterDateTextBox calendarTextBox inputWidget-input inputEnabled"]', current_date)
    
    # Establecer la fecha futura en el campo "Hasta"
    set_date('//div[@class="inputWidget timeIntervalSearcher-endDateWidget"]//input[@class="gwt-TextBox filterDateTextBox calendarTextBox inputWidget-input inputEnabled"]', future_date)
    
    # Hacer clic en el botón de búsqueda
    search_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@type="button" and contains(@class, "philaxButton-button") and .//i[contains(@class, "fa-search")]]')))
    driver.execute_script("arguments[0].click();", search_button)
    
    # Esperar a que el archivo se descargue completamente
    time.sleep(60) 
    
    # Hacer clic en el botón de exportación
    export_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[contains(@class, "agendaAppointmentsStatisticsByTimePanel-excelButton")]//button[@type="button" and contains(@class, "philaxButton-button")]')))
    driver.execute_script("arguments[0].click();", export_button)
    
    # Añadir un tiempo de espera de 30 segundos entre las descargas
    time.sleep(5)
    
    # Incrementar la fecha inicial en 300 días para el siguiente ciclo
    start_date += timedelta(days=300)

# Cerrar el navegador al finalizar todos los ciclos
driver.quit()
