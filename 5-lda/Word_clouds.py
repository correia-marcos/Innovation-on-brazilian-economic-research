"""
Script for WordCloud generation.

Done the final step of modeling: use topics divided by year and by
research area at LDA

"""

import pandas as pd
# from artifici_lda.lda_service import train_lda_pipeline_default
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
# import os
from wordcloud import WordCloud
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns

sns.set()
% matplotlib inline
# it is necessary to go to this directory to read the artifici_lda module
# os.chdir('C:/Users/Usuário/Projects/monografia/preprocessing/')


def mysplit3(s) -> str:
    """Do a simple split os numbers and letters."""
    head = s.rstrip('0123456789')
    tail = s[len(head):].zfill(2)
    return head + tail


local = r'C:\Users\Usuário\Projects\monografia\dados\data_final'
corpus = pd.read_pickle(f'{local}/corpus_cleaned2.pkl')

data = pd.read_pickle(f'{local}/data_final_v2.pkl')
data.code_area = data['code_area'].astype(str).apply(lambda x: mysplit3(x))

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

corpus_en = pd.DataFrame(
    df[df.linguagem == 'en'].texts,
    index=df.index
    ).dropna()

# corpus_en_list = corpus_en.texts.tolist()


stopwords = pickle.load(open(f'{local}\\stopwords_total.pkl', 'rb'))
stopwords.append('modelo')
stopwords.append('resultado')
stopwords.append('como')
stopwords.append('para')
stopwords.append('model')

pickle.dump(stopwords, open(f'{local}\\stopwords_total.pkl', 'wb'))


def DTM_wordcloud(df_column, linguagem, stopwords):
    """Does the entire process of generating the matrix of document terms.

       Performs the following activities:
                                      generation of TfidfVectorizer,
                                      DocumentTermMatrix generation
    """
    tfidf = TfidfVectorizer(stop_words=stopwords)
    base = tfidf.fit_transform(df_column)
    data_dtm = pd.DataFrame(base.toarray(),
                            columns=tfidf.get_feature_names())
    data_dtm.index = df_column.index

    return data_dtm


data_word_en = DTM_wordcloud(corpus_en.texts, 'english', stopwords)
data_word_pt = DTM_wordcloud(corpus_pt.texts, 'portuguese', stopwords)

# data_word_en = data_word_en.transpose()
# data_word_pt = data_word_pt.transpose()

# =============================================================================
# Quality of Topic modelling verification
# =============================================================================

top_dict = {}
for c in data_word_en.columns:
    top = data_word_en[c].sort_values(ascending=False).head(30)
    top_dict[c] = list(zip(top.index, top.values))


words = []
for doc in data_word_en.columns:
    top = [word for (word, count) in top_dict[doc]]
    for t in top:
        words.append(t)

counter = Counter(words).most_common()

# =============================================================================
# Generating the bases specified by area and language
# =============================================================================
groups = df.groupby(['linguagem', 'code_area'])
dfs = dict(tuple(groups))
dfs.pop(('es', 'i06'))
dfs.pop(('es', 'i02'))


base_en = [f'wordcloud_en_i{x}' for x in range(1, 14)]
base_pt = [f'wordcloud_pt_i{x}' for x in range(1, 14)]

base_total = base_en + base_pt


areas = data.reset_index()[['Área', 'code_area']].values.astype(str).tolist()

dicio = dict()

for sub in areas:
    dicio[sub[1]] = sub[0]
dicio.pop('nan00')


def WordcloudsEn(dicionario):
    """Generate English papers Wordclouds.

    It is bad defined, since it uses variable previously defined, what can
    be very messy.
    """
    plt.rcParams['figure.figsize'] = [20, 10]
    plt.rcParams['axes.titlesize'] = 'medium'
    plt.rcParams['figure.dpi'] = 125.0
    valor = 0
    wc = WordCloud(stopwords=stopwords, background_color="white",
                   colormap="Dark2", max_font_size=150, random_state=42)

    for keys in sorted(dicionario):
        lingua, sigla = keys
        print(str(dicio[sigla]) + f' ({lingua})')
        if lingua == 'en':
            cloud = corpus_en[corpus_en.index.isin(
                dfs[lingua, sigla].index)]
            wc.generate(' '.join(cloud.texts))
            valor += 1

        plt.subplot(2, 6, valor)
        plt.imshow(wc, interpolation="bilinear")
        plt.axis("off")
        plt.title(str(dicio[sigla]))
        # plt.tight_layout()


def WordcloudsPt():
    """Generate English papers Wordclouds.

    It is bad defined, since it uses variable previously defined, what can
    be very messy.
    """
    plt.rcParams['figure.figsize'] = [20, 10]
    plt.rcParams['axes.titlesize'] = 'medium'
    plt.rcParams['figure.dpi'] = 155.0
    valor = 0
    wc = WordCloud(stopwords=stopwords, background_color="white",
                   colormap="Dark2", max_font_size=150, random_state=42)

    for keys in sorted(dfs):
        lingua, sigla = keys
        print(str(dicio[sigla]) + f' ({lingua})')
        if lingua == 'pt':
            cloud = corpus_pt[corpus_pt.index.isin(
                dfs[lingua, sigla].index)]
            wc.generate(' '.join(cloud.texts))
            valor += 1

            plt.subplot(4, 4, valor)
            plt.imshow(wc, interpolation="bilinear")
            plt.axis("off")
            plt.title(str(dicio[sigla]))
            # plt.tight_layout()


WordcloudsEn(dfs)
WordcloudsPt()
