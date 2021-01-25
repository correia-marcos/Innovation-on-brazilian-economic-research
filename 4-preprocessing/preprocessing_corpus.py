"""
Script for pre-processing e CORPUS generation.

What is was done: Removal of references from papers,
                  Convertion of textos for onlu small letters (lowercase)
                  Removal of pontuantions

References are bad for Topic Modelling.
IMPORTANT: As it was also possible to see in the script "finding_languagues.py"
the conversion from pdf to txt causes some problems in some articles. We were
unable to identify the source of the error, but the conversion (in UTF-8)
generated symbols that were not encoded correctly.
Exemple: --> 
Exemple2: some words loose spaces --> emrelação nateoria

See the folowing link to understand more:
https://github.com/aboSamoor/polyglot/issues/71
"""

import os
import io
import glob
import pandas as pd
import re
import regex
import string
# from unidecode import unidecode


os.chdir('C:\\Users\\Usuário\\Projects\\monografia\\preprocessing')


def remove_bad_chars(text):
    """
    Take away bad chars.

    Some documents had issues related to decoding (with UTF-8).

    This function tries to writes off this problems, eliminating "Cc" and
    "Cs" category of chars from .txt files.
    """
    RE_BAD_CHARS = regex.compile(r"\p{Cc}|\p{Cs}")
    return RE_BAD_CHARS.sub("", text)


os.chdir('C:\\Users\\Usuário\\Projects\\monografia\\dados\\txt_files')
txt_files = sorted(glob.glob('*.txt'))

# os.mkdir(r'C:\\Users\\Usuário\\Projects\\monografia\\dados\\txt_files_updated')

# =============================================================================
# Removing references from papers
# =============================================================================
# pattern1 = re.compile(r'introdução|introduccion|introducción|introduction')

pattern_referencias = re.compile(r"""(bibliografía|references|reference|
                      referencias bibliograficas|bibliography|
                      archives?|archive|referências bibliográficas|
                      referências|refer.ncias|bibliografias|
                      referencia bibliografica|bibliografia|
                      referencia bibliográfica|referência bibliografica|
                      fontes primárias)""")


for txt in txt_files:
    os.chdir('C:/Users/Usuário/Projects/monografia/dados/txt_files')
    with io.open(txt, 'r', encoding='utf-8') as text:
        artigo = text.readlines()
        artigo = [x.strip() for x in artigo]
        texto_final = u''.join(map(str, artigo))
        # Remove chars that have UTF-8 errors
        texto_final = remove_bad_chars(texto_final)
        # Lowercase
        texto_final = texto_final.lower()
        # References removal
        texto_div = re.split(pattern_referencias, texto_final)
        if len(texto_div) > 1:
            texto_update = u''.join(map(str, texto_div[:-2]))
        else:
            texto_final = texto_final.lower()

    os.chdir('C:/Users/Usuário/Projects/monografia/dados/txt_files_updated')

    with io.open(txt, 'w', encoding='utf-8') as text:
        text.write(texto_update)


# =============================================================================
# CORPUS generation
# =============================================================================

os.chdir('C:/Users/Usuário/Projects/monografia/dados/txt_files_updated')
txt_files = sorted(glob.glob('*.txt'))

txts = []
textos = []
for txt in txt_files:
    doc = os.path.splitext(txt)[0]
    txts.append(doc)
    with io.open(txt, 'r', encoding='utf-8') as text:
        artigo = text.readlines()
        textos.append(artigo)

corpus = pd.DataFrame(textos, index=txts, columns=['texts'])
local = r'C:\Users\Usuário\Projects\monografia\dados\data_final'
corpus.to_pickle(f'{local}/corpus.pkl')

# =============================================================================
# General part of pre-processing, STEMMING and LDA generation
# =============================================================================


def clean_text_round1(text):
    """
    Clean up text data.

    Make text lowercase, remove text in square brackets, remove
    punctuation, remove digits in general, remove urls, remove
    emails and remove "" caracteres.
    unidecode = If there is a non ASCII caracter, turn it into
    ASCII readable --> not used because it hinders the Stemming.
    """
    text = text.lower()
    text = re.sub(r'\[.*?\]', '', text)
    #  r'[%s]' % re.escape(string.punctuation) remove accents from words,
    # which hinders the Stemming process.
    # text = re.sub(r'[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub(r'[!,:\-;\.\?\(\)]', '', text)
    text = ''.join(i for i in text if not i.isdigit())
    text = re.sub(r'^https?:\/\/.*[\r\n]*', '', text)
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[‘’“”…]', '', text)
    text = re.sub('\n', '', text)
    # unidecode(text) remove accents from words, which hinders Stemming process
    # so it was not done.
    # text = unidecode(text)

    return text


round1 = lambda x: clean_text_round1(x)

corpus_cleaned = pd.DataFrame(corpus['texts'].apply(round1), index=txts,
                              columns=['texts'])
corpus_cleaned.to_pickle(f'{local}/corpus_cleaned.pkl')

# Lists are easier to vizualize since the memory size of a series in Python is
# much bigger. We vizualize the quality of the function if this.
texto_avaliar = corpus_cleaned.texts.tolist()


def clean_text_round2(text):
    """
    Clean up text data.

    Do what clean_text_round1 does, adding:
    Remove pontuations, except accents.
    Remove words if less than 4 letters
    Remove some special chars commom in papers
    """
    remove = string.punctuation
    remove = remove.replace("´", "")
    remove = remove.replace("^", "")
    remove = remove.replace("~", "")
    remove = remove.replace("`", "")
    text = re.sub(r'[%s]' % re.escape(remove), '', text)
    text = text.replace("𝑐𝑜𝑣", '')
    text = text.replace('𝑥𝑖', '')
    text = text.replace('𝐸(𝑦|𝑥)', '')
    text = text.replace('𝑝𝑙𝑖𝑚', '')
    text = re.sub(r'\b\w{1,3}\b', '', text)
    text = text.lower()
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'[!,:\-;\.\?\(\)]', '', text)
    text = ''.join(i for i in text if not i.isdigit())
    text = re.sub(r'^https?:\/\/.*[\r\n]*', '', text)
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[‘’“”…]', '', text)
    text = re.sub('\n', '', text)

    return text

round2 = lambda x: clean_text_round2(x)

corpus_cleaned = pd.DataFrame(corpus['texts'].apply(round2),
                              index=corpus.index,
                              columns=['texts'])
textos_avaliar2 = corpus_cleaned.texts.tolist()
corpus_cleaned.to_pickle(f'{local}/corpus_cleaned2.pkl')


def clean_text_round3(text):
    """
    Clean up text data.

    Do what clean_text_round1 does, adding:
    Remove pontuations, except accents.
    Remove words if less than 3 letters
    Remove some special chars commom in papers
    """
    remove = string.punctuation
    remove = remove.replace("´", "")
    remove = remove.replace("^", "")
    remove = remove.replace("~", "")
    remove = remove.replace("`", "")
    text = re.sub(r'[%s]' % re.escape(remove), '', text)
    text = text.replace("𝑐𝑜𝑣", '')
    text = text.replace('𝑥𝑖', '')
    text = text.replace('𝐸(𝑦|𝑥)', '')
    text = text.replace('𝑝𝑙𝑖𝑚', '')
    text = re.sub(r'\b\w{1,2}\b', '', text)
    text = text.lower()
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'[!,:\-;\.\?\(\)]', '', text)
    text = ''.join(i for i in text if not i.isdigit())
    text = re.sub(r'^https?:\/\/.*[\r\n]*', '', text)
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[‘’“”…]', '', text)
    text = re.sub('\n', '', text)

    return text


round3 = lambda x: clean_text_round3(x)

corpus_cleaned = pd.DataFrame(corpus['texts'].apply(round3),
                              index=corpus.index,
                              columns=['texts'])
textos_avaliar3 = corpus_cleaned.texts.tolist()
corpus_cleaned.to_pickle(f'{local}/corpus_cleaned3.pkl')
