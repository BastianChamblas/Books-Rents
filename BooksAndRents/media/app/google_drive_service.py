import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Ruta al archivo de cuenta de servicio
SERVICE_ACCOUNT_FILE = r'C:\BooksAndRents\app\client_secrets.json'  # Usando una cadena sin procesar
SCOPES = ['https://www.googleapis.com/auth/drive']

def get_drive_service():
    """Autentica y devuelve un servicio de Google Drive usando una cuenta de servicio."""
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)
    return service

def get_file_url(file_id_or_url):
    """Devuelve la URL directa de visualización para un archivo de Google Drive.

    Puede recibir el `file_id` directamente o una URL completa.
    """
    # Si el parámetro contiene una URL completa, extrae el `file_id`
    if "https://drive.google.com" in file_id_or_url:
        # Extrae el ID cuando la URL tiene el formato completo de Google Drive
        if "id=" in file_id_or_url:
            file_id = file_id_or_url.split("id=")[1].split("&")[0]
        elif "/file/d/" in file_id_or_url:
            file_id = file_id_or_url.split("/file/d/")[1].split("/view")[0]
        else:
            return ""  # Si la URL no es válida, regresa un string vacío
    else:
        # Si solo se pasa el `file_id`, úsalo directamente
        file_id = file_id_or_url

    # Genera la URL directa de visualización
    return f"https://drive.google.com/uc?export=view&id={file_id}"

def list_files():
    """Ejemplo de cómo listar archivos en Google Drive."""
    service = get_drive_service()
    results = service.files().list(pageSize=10).execute()
    items = results.get('files', [])
    return items
