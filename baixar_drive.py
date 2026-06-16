import os
import re
import gdown

PASTA_DOWNLOAD = "downloads"
ARQUIVO_LINKS = "links.txt"

os.makedirs(PASTA_DOWNLOAD, exist_ok=True)


def extrair_id(link):
    padroes = [
        r"id=([A-Za-z0-9_-]+)",
        r"/d/([A-Za-z0-9_-]+)",
        r"file/d/([A-Za-z0-9_-]+)"
    ]

    for p in padroes:
        m = re.search(p, link)
        if m:
            return m.group(1)

    return None


with open(ARQUIVO_LINKS, encoding="utf-8") as f:
    links = [linha.strip() for linha in f if linha.strip()]

print(f"{len(links)} links encontrados.\n")

for link in links:

    file_id = extrair_id(link)

    if not file_id:
        print(f"Link inválido: {link}")
        continue

    url = f"https://drive.google.com/uc?id={file_id}"

    try:
        gdown.download(
            url=url,
            output=PASTA_DOWNLOAD,
            quiet=False,
            fuzzy=True
        )

    except Exception as e:
        print(e)

print("Finalizado.")
