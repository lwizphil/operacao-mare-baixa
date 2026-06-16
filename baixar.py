import os
import re

from concurrent.futures import ThreadPoolExecutor

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

SERVICE_ACCOUNT_FILE = "credentials.json"

DOWNLOAD_FOLDER = "downloads"

LINKS_FILE = "links.txt"

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=SCOPES,
)

service = build("drive", "v3", credentials=credentials)


def extrair_id(link):

    padroes = [
        r"id=([A-Za-z0-9_-]+)",
        r"/d/([A-Za-z0-9_-]+)"
    ]

    for p in padroes:
        m = re.search(p, link)
        if m:
            return m.group(1)

    return None


def baixar(link):

    file_id = extrair_id(link)

    if file_id is None:
        print("Link inválido:", link)
        return

    try:

        metadata = service.files().get(
            fileId=file_id,
            fields="name"
        ).execute()

        nome = metadata["name"]

        caminho = os.path.join(DOWNLOAD_FOLDER, nome)

        request = service.files().get_media(fileId=file_id)

        with open(caminho, "wb") as arquivo:

            downloader = MediaIoBaseDownload(arquivo, request)

            done = False

            while not done:
                status, done = downloader.next_chunk()

        print("OK:", nome)

    except Exception as e:
        print("ERRO:", file_id, e)


with open(LINKS_FILE, encoding="utf-8") as f:

    links = [
        linha.strip()
        for linha in f
        if linha.strip()
    ]

print(f"{len(links)} arquivos encontrados.")

with ThreadPoolExecutor(max_workers=20) as executor:

    executor.map(baixar, links)

print("Downloads finalizados.")
