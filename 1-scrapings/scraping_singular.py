"""
Script for scraping.

Scraping links, names of articles, coautors, university and area of submission
in the ANPEC Meeting. Link:
https://en.anpec.org.br/previous-editions.php
This script was made to deal with specific issues. Por example, the html
containing 2015 papers is very different from the others. It is treated here.
Also, 2017 papers specific issues were dealt here.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os


# Download pagina

url_2017 = 'https://en.anpec.org.br/previous-editions/2017/artigos-2017.html'
url_2015 = 'https://en.anpec.org.br/previous-editions/2015/artigos-2015.html'


def scrape_2017_files(url, local):
    """
    Scraping 2017 html file and getting all the info required.

    We resolve the problem with 2017 html. Some articles just didn't have
    any link to download.
    This function will do everthing: from scraping to creating the csv data.
    Parameters
    ----------
    url : STRING
        2017 html.
    local : STRING
        Directory in which the GIT project was saved. Just need the root!!!

    Returns
    -------
    None.
    """
    r = requests.get(url)

    # Parsing html page
    soup = BeautifulSoup(r.text, 'html.parser')
    # print(soup.prettify())
    # tags_a = [i.a for i in soup.find_all('li')]

    areas = [i.a.get_text().strip() for i in
             soup.find_all('h4', {'class': "panel-title"})]

    # Getting links e articles title

    try:
        links = [a['href'] for a in soup.find_all('a', href=True) if a.text]
    except TypeError:
        pass

    try:
        links_nomes = [x.get_text() for x in soup.find_all('li')]
    except AttributeError:
        pass

    # List of autors and universities
    pre_autor = [x.get_text(separator='\n') for x in soup.find_all('li')]
    autor_uni = [i.split('\n') for i in pre_autor]
    autores_e_enti = []
    links_nomes = []

    for i in range(0, len(autor_uni)):
        try:
            autores_e_enti.append(autor_uni[i][1])
        except IndexError:
            pass

    for i in range(0, len(autor_uni)):
        try:
            links_nomes.append(autor_uni[i][0])
        except IndexError:
            pass
    # We'll remove papers without href. This was a process "made by hand",
    # searching through the html.
    # Actually important cause DataFrame require same lengh of all lists.

    links_nomes.remove("THE CHINESE CATCHING UP: A CLASSICAL DEVELOPMENTALIST"
                       + " APPROACH")
    autores_e_enti.remove("ELIAS MARCO KHALIL JABBOUR (UERJ) - LUIZ FERNANDO "
                          + "DE PAULA (UERJ)")
    links_nomes.remove("ANÁLISE DOS LEILÕES DE TRANSMISSÃO DE ENERGIA ELÉTRICA"
                       + " UTILIZANDO ENDOGENOUS SWITCHING REGRESSION MODEL" +
                       " COM ABORDAGEM CÓPULAS ")
    # autores_e_enti.remove("WASHINGTON MARTINS DA SILVA (UCB) - OSVALDO "
    #                       + "CANDIDO (UCB)")
    links_nomes.remove("INVESTMENT POLICIES, DEVELOPMENT FINANCE AND ECONOMIC"
                       + " TRANSFORMATION: LESSONS FROM BNDES")
    autores_e_enti.remove("JOÃO CARLOS FERRAZ (UFRJ/IE) - LUCIANO COUTINHO"
                          + " (UNICAMP/IE)")

    # Finally, clean incorrect data from "links" for only containing hrefs.

    links = [i for i in links if not '#' in i]

    # Creating DataFrame
    data = pd.DataFrame(
        {
            'título_2017': links_nomes,
            'links_2017': links,
            'autores_2017': autores_e_enti,
        }
    )
    data.head()

    # Selecting only urls with "docx", "doc" and "pdf"
    data = data[data.links_2017.str.contains(".docx?$|.pdf$")]
    data.head()

    # Getting the area code with link info
    data.loc[:, "code_area"] = data.links_2017.str.\
        extract(r"(?P<area>\/i[0-9]{1,2})")['area'].str.replace(r"\/", "")
    data.head()

    # Creating dict for Area and area code
    areas_df = pd.DataFrame(
        {
            'code_area': [f'i{n}' for n in range(1, 14)],
            'area': areas
        }
    )

    # areas_df.head()

    # Adding Area in data
    data = pd.merge(left=data, right=areas_df, on='code_area', how='outer')

    # Exporting resultados
    path_out = "./dados/raw/links_2017.csv"
    os.chdir(local)
    data.to_csv(path_out, sep=';', index=False, encoding='UTF-8')


# =============================================================================
# Scrape 2015
# =============================================================================

def scrape_2015_files(url, local):
    """
    Scraping 2017 html file and getting all the info required.

    We resolve the problem with 2017 html. Some articles just didn't have
    any link to download.
    This function will do everthing: from scraping to creating the csv data.
    One little difference with scrape_2017_files: this one uses 2017 url to
    know what is the name of each area (since it doesn't appeared on the html)


    Parameters
    ----------
    url : STRING
        2017 html.
    local : STRING
        Directory in which the GIT project was saved. Just need the root!!!

    Returns
    -------
    None.
    """
    r = requests.get(url)
    s = requests.get(url_2017)

    # Parsing html page
    soup = BeautifulSoup(r.text, 'html.parser')
    soup2 = BeautifulSoup(s.text, 'html.parser')
    # print(soup.prettify())
    # tags_a = [i.a for i in soup.find_all('li')]

    areas = [i.a.get_text().strip() for i in
             soup2.find_all('h4', {'class': "panel-title"})]

    # Getting links e articles title

    try:
        links = [a['href'] for a in soup.find_all('a', href=True) if a.text]
    except TypeError:
        pass

    # This html doesn't have any autors our universities info. In part 6, this
    # problem were resolved by google searching (by hand).
    try:
        titles = [x.get_text() for x in soup.find_all('a')]
    except AttributeError:
        pass

    # Finally, clean incorrect data from "links" for only containing hrefs.

    links = [i for i in links if not '#' in i]

    # Creating DataFrame
    data = pd.DataFrame(
        {
            'título_2015': titles,
            'links_2015': links,
        }
    )
    # data.head()

    # Selecting only urls with "docx", "doc" and "pdf"
    data = data[data.links_2015.str.contains(".docx?$|.pdf$")]
    # data.head()

    # Getting the area code with link info
    data.loc[:, "code_area"] = data.links_2015.str.\
        extract(r"(?P<area>\/i[0-9]{1,2})")['area'].str.replace(r"\/", "")
    # data.head()

    # Creating dict for Area and area code
    areas_df = pd.DataFrame(
        {
            'code_area': [f'i{n}' for n in range(1, 14)],
            'area': areas
        }
    )

    # areas_df.head()

    # Adding Area in data
    data = pd.merge(left=data, right=areas_df, on='code_area', how='outer')
    data = data.drop(data.tail(1).index)

    # Exporting resultados
    path_out = "./dados/raw/links_2015.csv"
    os.chdir(local)
    data.to_csv(path_out, sep=';', index=False, encoding='UTF-8')

# =============================================================================
# __main__
# =============================================================================

# Change the second argument of scrape_2017_files and scrape_2017_files
# in order to get the correct directory where the root of the project is
# located.


if __name__ == '__main__':
    scrape_2017_files(url_2017, 'C:\\Users\\Usuário\\Projects\\monografia')
    scrape_2015_files(url_2015, 'C:\\Users\\Usuário\\Projects\\monografia')
