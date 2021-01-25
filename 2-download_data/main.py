"""Main script to really download papers."""

import pandas as pd
from download_data.download_data import download_data, export_url_erro

# Weird attachement of 2015 html was not downloaded.


def download_artigos():
    """Make the download on the correct folders previous created."""
    # Change "local" variable to be the correct directory tree
    local = 'C:/Users/Usuário/Projects/monografia'
    path_data = [local + f"/dados/raw/links_{x}.csv"
                 for x in reversed(range(2013, 2020))]
    w = 0
    for j in reversed(range(2013, 2020)):
        dados = pd.read_csv(path_data[w], sep=';')

        # Creating id to docs
        dados['id_doc'] = [f'doc{i}' for i in range(1, dados.shape[0] + 1)]
        dados.to_csv(local + f"/dados/raw/data-index-{j}.csv",
                     sep=';', index=False)

        # Preparing links and paths to download
        links = dados[f'links_{j}'].to_list()
        extensao = dados[f'links_{j}'].str.extract(r"(?P<ext>.docx?$|.pdf$)")
        ['ext']
        extensao = extensao.ext.to_list()
        docs_id = dados.id_doc.to_list()
        paths = [local + f"/dados/files/docs_{j}/{doc}{ext}" for doc, ext
                 in zip(docs_id, extensao)]

        # Download data
        urls_erro = [download_data(url, path, silence=False)
                     for url, path in zip(links, paths)]

        # Saving urls of urls that were not downloaded
        path_url_erro = local + "/dados/files/url-erro.csv"
        export_url_erro(urls_erro, path_url_erro)
        w += 1

    return True


def main():
    """Do the download finally."""
    download_artigos()
    return None


if __name__ == '__main__':
    main()
