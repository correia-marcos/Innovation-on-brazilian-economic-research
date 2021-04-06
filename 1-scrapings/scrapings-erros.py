"""
This script resolve a problem with the scraping.py script.

The scraping.py couldn't get the url for downloading ".doc" papers. This is
an old extesion of microsoft word that is not used no more. Is a problem
regards old computer from researchers that was not previously thought.

problems with .doc papers just ocorred in three years
"""

import os
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Change to the correct Directory tree where is located the raw folder!
root = os.path.abspath(os.curdir)
os.chdir(f'{root}/dados/raw')

data_2014 = pd.read_csv('data-index-2014.csv', sep=';')
data_2016 = pd.read_csv('data-index-2016.csv', sep=';')
data_2018 = pd.read_csv('data-index-2018.csv', sep=';')

urls = [f"https://en.anpec.org.br/previous-editions/{x}/artigos-{x}.html" for x
        in [2014, 2016, 2018]]
j = 0

# This is the algorithm base: it'll repeat operations until all of links
# were scraped and processed. "j" is used to control what html is being parsed.

for w in [2014, 2016, 2018]:
    url = urls[j]

    r = requests.get(url)

    # Parsing the html page
    soup = BeautifulSoup(r.text, 'html.parser')
    print(soup.prettify())

    areas = [i.a.get_text().strip() for i in
             soup.find_all('h4', {'class': "panel-title"})]

    # Getting links and title of papers
    tags_a = [i.a for i in soup.find_all('li')]

    try:
        links = [x['href'] for x in tags_a]
    except TypeError:
        pass

    try:
        links_nomes = [x.get_text() for x in tags_a]
    except AttributeError:
        pass

    # Getting a list with autors and universities
    pre_autor = [x.get_text(separator='\n') for x in soup.find_all('li')]
    autor_uni = [i.split('\n') for i in pre_autor]
    autores_e_enti = []

    for i in range(0, len(autor_uni)):
        try:
            autores_e_enti.append(autor_uni[i][1:])
        except IndexError:
            pass

    # This list is smaller than the other ones, so we did a rule to get back
    # from the original size (necessary for a DataFrame):
    while(len(links_nomes) > len(autores_e_enti)):
        autores_e_enti.insert(0, '')

    # the variable "autores_e_enti" is a list of lists, but we would like to be
    # a string. Because of that, we first strip spaces and get together the
    # remaining values:

    for sublists in autores_e_enti:
        for string in sublists:
            string.rstrip()

    autores_e_enti = [' - '.join(i) for i in autores_e_enti]

    # DataFrame
    data = pd.DataFrame(
        {
            f'título_{w}': links_nomes,
            f'links_{w}': links,
            f'autores_e_universidades_{w}': autores_e_enti
        }
    )
    data.head()

    # Selecting only "doc"
    data = data[data[f'links_{w}'].str.contains(".doc$")]
    data.head()

    # Getting the code area from the link of download
    data.loc[:, "code_area"] = data[f'links_{w}'].str.\
        extract(r"(?P<area>\/i[0-9]{1,2})")['area'].str.replace(r"\/", "")
    data.head()

    # Creating a Dataframe for code areas and the name of the area
    areas_df = pd.DataFrame(
        {
            'code_area': [f'i{n}' for n in range(1, 14)],
            'area': areas
        }
    )

    # areas_df.head()

    # Adding area to the DataFrame
    data = pd.merge(left=data, right=areas_df, on='code_area', how='outer')
    data = data.dropna()

    # Exporting

    path_out = f"data-{w}.csv"

    if w == 2014:
        data_2014 = data_2014.append(data, ignore_index=True)
        data_2014.to_csv(path_out, sep=';', index=False, encoding='UTF-8')

    elif w == 2016:
        data_2016 = data_2016.append(data, ignore_index=True)
        data_2016.to_csv(path_out, sep=';', index=False, encoding='UTF-8')

    else:
        data_2018 = data_2018.append(data, ignore_index=True)
        data_2018.to_csv(path_out, sep=';', index=False, encoding='UTF-8')

    j += 1


os.chdir(f'{root}')
# data_2019 = pd.read_csv('data-index-2019.csv', sep=';')
# link = ["https://www.anpec.org.br/encontro/2019/submissao/files_I/i8-304a77bc2497c3c956b98adc7804317f.doc"]
# autores = ['RÔMULO EUFROSINO DE ALENCAR RODRIGUES (UFPB) - EDWARD MARTINS COSTA (UFC) - GUILHERME IRFFI (UFC) - JOSÉ NEWTON REIS PIRES (UFC)']
# nome = ['EFEITOS DA CONSTRUÇÃO DE PARQUES EÓLICOS SOBRE INDICADORES ECONÔMICOS E FISCAIS DOS MUNICÍPIOS BRASILEIROS']
# area = ['Área 8 - Microeconomia, Métodos Quantitativos e Finanças']
# codigo = ['i8']
# id_doc = ['doc240']

# data2 = pd.DataFrame(
#     {
#          'título_2019': nome,
#          'links_2019': link,
#          'autores_e_universidades_2019': autores,
#          'code_area': codigo,
#          'area': area,
#          'id_doc': id_doc
#     }
#  )
# data_2019 = data_2019.append(data2, ignore_index=True)
# data_2019.to_csv('data-index-2019.csv', index=False, encoding='UTF-8')
