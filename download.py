import csv
import os
import re

import gdown

LINKS_FILE = "links.txt"
DOWNLOAD_DIR = "downloads"
LOG_DIR = "logs"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

def extrair_id(link):
    padroes = [
        r"id=([A-Za-z0-9_-]+)",
        r"/d/([A-Za-z0-9_-]+)"
    ]

    for padrao in padroes:
        resultado = re.search(padrao, link)
        if resultado:
            return resultado.group(1)

    return None

def baixar(link):

    file_id = extrair_id(link)

    if file_id is None:
        return [link, "ERRO", "ID inválido"]

    url = f"https://drive.google.com/uc?id={file_id}"

    try:

        nome = gdown.download(
            url=url,
            output=DOWNLOAD_DIR,
            quiet=False,
            fuzzy=True
        )

        return [link, "OK", nome]

    except Exception as e:

        return [link, "ERRO", str(e)]

links = []

with open(LINKS_FILE, encoding="utf8") as arquivo:

    for linha in arquivo:

        linha = linha.strip()

        if linha != "":
            links.append(linha)

resultado = []

for i, link in enumerate(links):

    print(f"{i+1}/{len(links)}")

    resultado.append(baixar(link))

with open("logs/relatorio.csv","w",newline="",encoding="utf8") as csvfile:

    writer = csv.writer(csvfile)

    writer.writerow(["Link","Status","Arquivo"])

    writer.writerows(resultado)

print("Finalizado.")
