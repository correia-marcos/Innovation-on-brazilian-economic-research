"""Script for functions that make download of the papers."""

import requests
import time
import os


def download_data(url, path, sleep=3, silence=True):
    """Download of the papers."""
    time.sleep(sleep)
    if not silence:
        print("| Download de: ", url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 \
        Safari/537.36'
    }

    # Treating errors
    try:
        r = requests.get(url, headers=headers)
        with open(path, 'wb') as f:
            f.write(r.content)
        url_erro = None
    except Exception as e:
        print(e)
        url_erro = url

    return url_erro


def export_url_erro(urls: list, path: str) -> None:
    """Error treatment."""
    urls = [url for url in urls if url]
    if len(urls) > 0:
        urls = pd.DataFrame({'url_erro': urls})
        urls.to_csv(path, sep=';', index=False, encoding='cp1252')

    return None


if __name__ == '__main__':
    import pandas as pd
    # Change the below line to the correct directory tree where "dados" folder
    # is located.
    os.chdir('C:\\Users\\Usuário\\Projects\\monografia\\dados')
    path_data = [f"raw/links_{x}.csv" for x
                 in reversed(range(2013, 2020))]

    for i in range(0, len(path_data)):
        dados = pd.read_csv(path_data[0], sep=';')
        dados = dados.head(5)

        # Creating id for docs
        dados['id_doc'] = [f'doc{i}' for i in range(1, dados.shape[0] + 1)]
        os.chdir('C:\\Users\\Usuário\\Projects\\monografia\\dados\\teste')
        dados.to_csv("data-index.csv", sep=';', index=False,
                     encoding='cp1252')

        # Preparing links and paths for download
        links = dados['links_2019'].to_list()
        extensao = dados.links_2019.str.extract(r"(?P<ext>.docx$|.pdf$)")
        ['ext']
        extensao = extensao.to_list()
        docs_id = dados.id_doc.to_list()
        paths = [f"dados/testes/{doc}{ext}" for doc, ext
                 in zip(docs_id, extensao)]

        # Download files
        urls_erro = [download_data(url, path, silence=False)
                     for url, path in zip(links, paths)]

        # Exporting urls com erro
        export_url_erro(urls_erro, "dados/testes/urls-erro.csv")
