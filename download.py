import os
import re
import csv
from concurrent.futures import ThreadPoolExecutor

import gdown

DOWNLOAD_FOLDER = "downloads"
LOG_FOLDER = "logs"

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
os.makedirs(LOG_FOLDER, exist_ok=True)

ARQUIVO_LOG = os.path.join(LOG_FOLDER, "relatorio.csv")

with open("links.txt", encoding="utf8") as f:
    links = [l.strip() for l in f if l.strip()]


def extrair_id(link):
    padroes = [
        r"id=([a-zA-Z0-9_-]+)",
        r"/d/([a-zA-Z0-9_-]+)"
    ]

    for p in padroes:
        m = re.search(p, link)
        if m:
            return m.group(1)

    return None


def baixar(link):

    file_id = extrair_id(link)

    if not file_id:
        return [link, "ERRO", "ID inválido"]

    url = f"https://drive.google.com/uc?id={file_id}"

    try:

        arquivo = gdown.download(
            url=url,
            output=DOWNLOAD_FOLDER,
            quiet=False
        )

        return [link, "OK", arquivo]

    except Exception as e:

        return [link, "ERRO", str(e)]


with ThreadPoolExecutor(max_workers=5) as executor:
    resultados = list(executor.map(baixar, links))

with open(ARQUIVO_LOG, "w", newline="", encoding="utf8") as csvfile:

    writer = csv.writer(csvfile)

    writer.writerow(["Link", "Status", "Arquivo"])

    writer.writerows(resultados)

print("Fim.")
