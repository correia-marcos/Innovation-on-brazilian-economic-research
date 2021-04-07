"""
The most general program for scraping html pages of articles.

Scraping links, names of articles, coautors, university of coautors
and area of submission in the ANPEC Meeting. Link:
https://en.anpec.org.br/previous-editions.php

This script gets the following informations: titles of articles, coautors and
universites attached to them, url for downlado of the paper, code area and
area of submission.
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

root = os.path.abspath(os.curdir)

urls = [f"https://en.anpec.org.br/previous-editions/{x}/artigos-{x}.html" for x
        in reversed(range(2013, 2020))]
j = 0

# This is the algorithm base: it'll repeat operations until all of links
# were scraped and processed. "j" is used to control what html is being parsed.

for w in reversed(range(2013, 2020)):
    # 2015 htlm page is different, see scraping_singular.py
    if j == 4:
        pass
    else:
        url = urls[j]

    r = requests.get(url)

    # Parsing the html page
    soup = BeautifulSoup(r.text, 'html.parser')
    print(soup.prettify())

    areas = [i.a.get_text().strip() for i in
             soup.find_all('h4', {'class': "panel-title"})]

    # Getting links and title of papers
    tags_a = [i.a for i in soup.find_all('li')]

    # In 2017, some of the papers didn't gave link to download :/ we did
    # a condition for this.
    #  (before was only 'links = [x['href'] for x in tags_a]')

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
            autores_e_enti.append(autor_uni[i][1])
        except IndexError:
            pass

    # This list is smaller than the other ones, so we did a rule to get back
    # from the original size (necessary for a DataFrame):
    while(len(links_nomes) > len(autores_e_enti)):
        autores_e_enti.insert(0, '')

    # DataFrame
    data = pd.DataFrame(
        {
            f'título_{w}': links_nomes,
            f'links_{w}': links,
            f'autores_e_universidades_{w}': autores_e_enti
        }
    )
    data.head()

    # Selecting only "docx" or "pdf" urls.
    data = data[data[f'links_{w}'].str.contains(".docx$|.pdf$")]
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
    data.head()

    # Exporting
    path_out = f"./dados/raw/links_{w}.csv"

    # Change for the directory where the root of the project is located!
    os.chdir(f'{root}')
    data.to_csv(path_out, sep=';', index=False, encoding='UTF-8')
    j += 1
