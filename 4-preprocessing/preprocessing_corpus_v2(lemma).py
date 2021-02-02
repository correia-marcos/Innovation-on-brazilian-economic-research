"""
Script for pre-processing e CORPUS generation.

What is was done: Removal of references from papers,
                  Convertion of textos for onlu small letters (lowercase)
                  Removal of pontuantions

References are bad for Topic Modelling.

VERY IMPORTANT: We have done 3 differents file convertions in order to take a
find the best way to handle convertion problems. As upset as it can be, our
first attempt (with pdftotext) was the best one! PDF are actually a quiet
challenging software and the pdfminer can't deal with some particulary issues.
See the below link for more information.
    https://github.com/euske/pdfminer/issues/39

VERY IMPORTANT2: The different between this script and the one before is that
it also have a lemmatizing process! There are other differences (this one
is wiser), but LEMMATIZATION is the main difference. The lemaatization was
made with Stanza, the second best project in lemmatization currently (2020).
More info in "lda_v2.py".

IMPORTANT: As it was also possible to see in the script "finding_languagues.py"
the conversion from pdf to txt causes some problems in some articles. We were
unable to identify the source of the error, but the conversion (in UTF-8)
generated symbols that were not encoded correctly.
* this is major problem in "pdfminer" library.
Exemple: --> 
Exemple2: some words loose spaces --> emrelação nateoria

See the following link to understand more:
https://github.com/aboSamoor/polyglot/issues/71


"""

import os
import io
import glob
import pandas as pd
import re
import regex
import string
import stanza
import logging
# from unidecode import unidecode

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.INFO)


def remove_bad_chars(text):
    """
    Take away bad chars.

    Some documents had issues related to decoding (with UTF-8).

    This function tries to writes off this problems, eliminating "Cc" and
    "Cs" category of chars from .txt files.
    """
    RE_BAD_CHARS = regex.compile(r"\p{Cc}|\p{Cs}")
    return RE_BAD_CHARS.sub(" ", text)


root = os.path.abspath(os.curdir)

txt_files = sorted(glob.glob('.\\dados\\txt_files/*.txt'))

# os.mkdir(r'C:\\Users\\Usuário\\Projects\\monografia\\dados\\txt_files_updated')


# =============================================================================
# Removing references from papers and CORPUS generation
# =============================================================================
# pattern1 = re.compile(r'introdução|introduccion|introducción|introduction')


def corpus_list(txt_files):
    """Create the base of a CORPUS database."""
    pattern_referencias = re.compile(r"""(\bbibliografía\b|\breferences\b|
                          \breference\b|
                          \bReferences\b|
                          \breferencias bibliograficas\b|\bbibliography\b|
                          \barchives?\b|\barchive\b|\bREFERÊNCIAS\b|
                          \breferências bibliográficas\b|
                          \breferências\b|\brefer.ncias\b|\bbibliografias\b|
                          \breferencia bibliografica\b|\bbibliografia\b|
                          \breferencia bibliográfica\b|
                          \breferência bibliografica\b|\bReferências\b|
                          \bReferências bibliográficas\b|
                          \bReferênciasBibliográficasBABA\b|
                          \bBibliografia\b|
                          \bReferências\b|
                          \bBibliography\b|
                          \bREFERENCES\b|
                          \bReferênciasBibliográficas\b|
                          \bReferências Bibliográficas\b|
                          \bREFERÊNCIAS BIBLIOGRÁFICASALICE\b|
                          \bReferências\b|
                          \bBibliografiaALBUQUERQUE\b|
                          \bReferencesACHILLADELIS\b|
                          \bReferências Bibliográficas\b|
                          \bREFERÊNCIAS\b|
                          \bREFERÊNCIASBRAGA\b|
                          \bREFERÊNCIAS\b
                          \bBIBLIOGRAFIA\b|
                          \bREFERÊNCIASAnthony\b
                          \bReferências bibliográficas\b|
                          \bfontes primárias\b|\breferências\b)""")
    txts = []
    textos = []
    for txt in txt_files:
        doc = os.path.splitext(txt)[0]
        txts.append(doc)
        with io.open(txt, 'r', encoding='UTF-8') as text:
            artigo = text.readlines()
            texto_final = u''.join(map(str, artigo))
            texto_final = texto_final.replace('', 'ff')
            # texto_final = texto_final.replace(' ', 'fi')
            # texto_final = texto_final.replace('', 'fi')
            texto_final = texto_final.replace('￿', ' ')
            # Remove chars that have UTF-8 errors
            texto_final = remove_bad_chars(texto_final)
            # Remove digits in general
            texto_final = ''.join(i for i in texto_final if not i.isdigit())
            # References removal
            texto_div = re.split(pattern_referencias, texto_final)
            if len(texto_div) > 1:
                # Arbitrary interception to prevent the removal of
                # important parts of the paper that used terms like "reference"
                # or other that is present in "pattern_referencias".
                # Looking at the size of references, it is actually a good
                # reference
                if len(texto_div[-1]) < 7000:
                    texto_update = u''.join(map(str, texto_div[:-2]))
                else:
                    texto_update = u''.join(map(str, texto_div))
            else:
                texto_update = texto_final
            textos.append(texto_update)

    index = [re.search(r'(doc[0-9]{3}_[0-9]{4})', txt).group() for txt in txts]

    return textos, index


textos, index = corpus_list(txt_files)

corpus = pd.DataFrame(textos, index=index, columns=['texts'])
local = r'.\dados\data_final'
corpus.to_pickle(f'{local}/corpus_v2.pkl')

# =============================================================================
# LEMMATIZATION
# =============================================================================

stanza.download('pt')
stanza.download('en')

data = pd.read_pickle(f'{root}/{local}/data_final_v2.pkl')

df = pd.concat([corpus, data], axis=1, sort=False)
df = df[df.texts.notna()]
df['docs'] = df.index
df['ano'] = df.docs.str.split('_')
df.loc[:, 'ano'] = df.ano.map(lambda x: x[1])

df = df.drop('docs', 1)
df = df.drop('autores_universi.', 1)
df = df.drop('Área', 1)
df = df.drop('tí­tulo', 1)

corpus_pt = pd.DataFrame(
    df[df.linguagem == 'pt'].texts,
    index=df.index
    ).dropna()
nlp_pt = stanza.Pipeline('pt', processors='tokenize,pos,lemma')

corpus_en = pd.DataFrame(
    df[df.linguagem == 'en'].texts,
    index=df.index
    ).dropna()
nlp_en = stanza.Pipeline('en', processors='tokenize,pos,lemma')


def lemmatize_sentence(sentence, lang):
    """Do the lemmatization process in Stanza."""
    lemma = ""
    if lang == 'en':
        for sent in nlp_en(sentence).sentences:
            for word in sent.words:
                lemma += word.lemma
                lemma += ' '
    elif lang == 'pt':
        for sent in nlp_pt(sentence).sentences:
            for word in sent.words:
                lemma += word.lemma
                lemma += ' '

    return lemma


list_corpus_en = corpus_en.texts.to_list()
list_corpus_pt = corpus_pt.texts.to_list()
teste = lemmatize_sentence(list_corpus_en[5], 'en')


corpus_en_lemma = [lemmatize_sentence(list_corpus_en[i], 'en') for i in
                   range(len(list_corpus_en))]

corpus_pt_lemma = [lemmatize_sentence(list_corpus_pt[i], 'pt') for i in
                   range(len(list_corpus_pt))]

corpus_en['texts_lemma'] = corpus_en_lemma
corpus_en.drop('texts', axis=1, inplace=True)
corpus_en = corpus_en.rename(columns={'texts_lemma': 'texts'})

corpus_pt['texts_lemma'] = corpus_pt_lemma
corpus_pt.drop('texts', axis=1, inplace=True)
corpus_pt = corpus_pt.rename(columns={'texts_lemma': 'texts'})

# =============================================================================
# General part of pre-processing
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
textos_avaliar = corpus_cleaned.texts.tolist()


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

# ============================================================================


def deEmojify(text):
    """Remove emotions (they happen in one or more papers).

    It doens't work in this texts :(
    """
    regrex_pattern = re.compile(pattern="["
                                u"\U0001F600-\U0001F64F"  # emoticons
                                u"\U0001F300-\U0001F5FF"  # symbols & graphs
                                u"\U0001F680-\U0001F6FF"  # map symbols
                                u"\U0001F1E0-\U0001F1FF""]+",
                                flags=re.UNICODE)
    return regrex_pattern.sub(r'', text)


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
    text = re.sub(r'[%s]' % re.escape(remove), ' ', text)
    text = text.replace("𝑐𝑜𝑣", ' ')
    text = text.replace('𝑥𝑖', ' ')
    text = text.replace('𝐸(𝑦|𝑥)', ' ')
    text = text.replace('𝑝𝑙𝑖𝑚', ' ')
    text = re.sub(r'\b\w{1,3}\b', ' ', text)
    text = text.lower()
    text = re.sub(r'\[.*?\]', ' ', text)
    text = re.sub(r'[!,:\-;\.\?\(\)]', ' ', text)
    text = ''.join(i for i in text if not i.isdigit())
    text = re.sub(r'^https?:\/\/.*[\r\n]*', ' ', text)
    text = re.sub(r'http\S+', ' ', text)
    text = re.sub(r'[‘’“”…]', ' ', text)
    text = re.sub('\n', ' ', text)
    text = re.sub('(e?mail|hotmail)', ' ', text)
    text = deEmojify(text)

    return text


round3 = lambda x: clean_text_round3(x)

# corpus_cleaned = pd.DataFrame(corpus['texts'].apply(round3),
#                               index=corpus.index,
#                               columns=['texts'])
corpus_cleaned_en = pd.DataFrame(corpus_en['texts'].apply(round3),
                                 index=corpus_en.index,
                                 columns=['texts'])
corpus_cleaned_pt = pd.DataFrame(corpus_pt['texts'].apply(round3),
                                 index=corpus_pt.index,
                                 columns=['texts'])

textos_avaliar3 = corpus_cleaned_en.texts.tolist()
textos_avaliar4 = corpus_cleaned_pt.texts.tolist()


# corpus_cleaned.to_pickle(f'{local}/corpus_cleaned3.pkl')
corpus_cleaned_en.to_pickle(f'{local}/corpus_cleaned4_en.pkl')
corpus_cleaned_pt.to_pickle(f'{local}/corpus_cleaned4_pt.pkl')
