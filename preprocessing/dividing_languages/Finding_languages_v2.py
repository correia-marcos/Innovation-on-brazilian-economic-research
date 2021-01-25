"""
Script to find the language that a given paper was written in.

IMPORTANT: We tried to do the language recognition with TextBlob, but it wasn't
extremely precise! We used "polyglot" library, which is very hard to install
in WINDOWS computers. We recommend to acess the following link:
    https://medium.com/@tlachacml/a-guide-for-using-polyglot-on-windows-8cbd8f97c7b0
it is necessary to clone github of the library besides other things.

Language recognition is essencial in the topic modelling part, since two
different topic models (for each language) was done on the next step.

This SCRIPT does:
    Language recognition
    Merge together all the yearly databases.
"""
from polyglot.text import Text
import os
import io
import glob
import pandas as pd
import numpy as np
# from textblob import TextBlob
import regex

# You need to go to the divind_languagues folder in order to read polyglot
# library!!!
# os.chdir('C:\\Users\\Usuário\\Projects\\monografia\\preprocessing\\
#           dividing_languages')
RE_BAD_CHARS = regex.compile(r"\p{Cc}|\p{Cs}")


def remove_bad_chars(text):
    """Remove bad convertion characters."""
    return RE_BAD_CHARS.sub("", text)


def mysplit2(s) -> str:
    """
    Divide a string in their numerical content and their letters.

    Only works for strings like ('abcde144141').
    """
    head = s.rstrip('0123456789')
    tail = s[len(head):].zfill(3)
    both = head + tail
    return str(both)


# Change the below "local" variable to correct specify the directory tree
local = 'C:/Users/Usuário/Projects/monografia/dados/data_final'
os.chdir('C:/Users/Usuário/Projects/monografia/dados/raw')
arquivos = glob.glob('data-index*.csv')


# By a mistake in our codes, data-index-2019.csv was imported with sep = ","
data = pd.read_csv(arquivos[-1], sep=',')
data.to_csv('data-index-2019.csv', sep=';', encoding='utf-8', index=False)


# By the way in which 2015 papers were presented in ANPEC site, we couldn't
# get the autors names. This is later resolved by searching the autors in
# Google (by hand).
data_2015 = pd.read_csv('data-index-2015.csv', sep=';')
data_2015.insert(2, 'autores', np.nan)
data_2015.to_csv('data-index-2015.csv', sep=';', index=False,
                 encoding='utf-8')


def create_finaldf(arquivos: list):
    """
    Criate the final database of the project.

    Essa servirá de referência para o topic modelling e outros processos.

    Parameters
    ----------
    arquivos : list
        List of csv files.

    Returns
    -------
    data_final: DataFrame with all the articles.

    """
    data_final = pd.DataFrame()
    for arquivo in arquivos:
        nome_arquivo = os.path.splitext(arquivo)[0]
        nome, info, ano = nome_arquivo.split('-')

        data = pd.read_csv(arquivo, sep=';')
        data.columns = ['tí­tulo', 'links', 'autores_universi.', 'code_area',
                        'Área', 'documento']
        data.documento = data.documento.apply(lambda value: mysplit2(value)
                                              + f'_{ano}')
        data_final = data_final.append(data, ignore_index=True)
        data_final = data_final.drop_duplicates()
        data_final = data_final.drop(columns=['links'])
        data_final.to_pickle(f'{local}/data_final.pkl')

    return data_final

# Change the below os.chdir!
os.chdir('C:\\Users\\Usuário\\Projects\\monografia\\dados\\txt_filesv2')
txt_files = glob.glob('*.txt')


txts = []
linguas = []
for txt in txt_files:
    doc = os.path.splitext(txt)[0]
    txts.append(doc)
    with io.open(txt, 'r', encoding='utf-8') as text:
        artigo = text.readlines()
        texto_final = ''.join(map(str, artigo)).strip()
        texto_final = texto_final.replace('', 'ff')
        # texto_final = texto_final.replace('', 'fi')
        # texto_final = texto_final.replace('', 'fi')
        texto_final = texto_final.replace('￿', '')

        try:
            b = Text(texto_final)
            lingua = b.language.code
            linguas.append(lingua)
        except:
            texto_final = remove_bad_chars(texto_final)
            b = Text(texto_final)
            lingua = b.language.code
            linguas.append(lingua)


linguagem = pd.Series(linguas, index=txts, name='linguagem')

data_final = pd.read_pickle(f'{local}/data_final.pkl')
df_concat = pd.concat([data_final.set_index('documento'),
                       linguagem.to_frame()], axis=1,
                      sort=False)
df_concat.to_pickle(f'{local}/data_final_v2.pkl')

teste = pd.read_pickle(f'{local}/data_final_v2.pkl')
