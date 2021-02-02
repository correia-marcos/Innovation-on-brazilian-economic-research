"""
Script for Topic Modelling.

This is, maybe, the most important script of all.
"""
import os
import pandas as pd
# from artifici_lda.lda_service import train_lda_pipeline_default
import pickle
import scipy.sparse
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim import matutils, corpora
from gensim.models import LdaMulticore, CoherenceModel
from nltk import word_tokenize
# is necessary to go to this directory!
os.chdir('C:/Users/Usuário/Projects/monografia/preprocessing/')
artifici_lda.logic.stemmer import Stemmer

root = os.path.abspath(os.curdir)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.INFO)

local = r'/dados/data_final'
corpus = pd.read_pickle(f'{root}/{local}/corpus_cleaned3.pkl')

data = pd.read_pickle(f'{root}{local}/data_final_v2.pkl')

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

corpus_en['tokenized'] = corpus_en['texts'].apply(word_tokenize)
corpus_pt['tokenized'] = corpus_pt['texts'].apply(word_tokenize)


stopwords = pickle.load(open(f'{local}\\stopwords_total.pkl', 'rb'))

# =============================================================================
# Teste com a biblioteca Multilingual - usa um Pipeline
# houve problemas com esssa geração dos dados
# fizemos testes posteriores e o resultado era muito diferente ao que
#  foi salvo nos documentos em pkl file
# =============================================================================
# transformed_comments_pt, top_comments_pt, _1_grams_pt, _2_grams_pt = \
#     train_lda_pipeline_default(corpus_pt, n_topics=15, language='portuguese',
#                                stopwords=stopwords_total)

# transformed_comments_en, top_comments_en, _1_grams_en, _2_grams_en = \
#     train_lda_pipeline_default(corpus_en.texts.values, n_topics=15,
#                                language='english', stopwords=stopwords_total)

# os.chdir(local)
# pickle.dump(transformed_comments_pt, open('transformed_pt.pkl', 'wb'))
# pickle.dump(transformed_comments_en, open('transformed_en.pkl', 'wb'))
# pickle.dump(top_comments_pt, open('topcoments_pt.pkl', 'wb'))
# pickle.dump(top_comments_en, open('topcoments_en.pkl', 'wb'))
# pickle.dump(_1_grams_pt, open('_1_grams_pt.pkl', 'wb'))
# pickle.dump(_1_grams_en, open('_1_grams_en.pkl', 'wb'))
# pickle.dump(_2_grams_pt, open('_2_grams_pt.pkl', 'wb'))
# pickle.dump(_2_grams_en, open('_2_grams_en.pkl', 'wb'))


# transformed_en = pickle.load(open('transformed_en.pkl', 'rb'))

# =============================================================================
# Biliotecas gerais (sklearn, lda...)
# =============================================================================


def Gen_DocumentTermMatrix(df_column, linguagem, stopwords,
                           quer_stemming='True'):
    """Faz todo o processo de geração da matrix de termos dos documentos.

    Realiza as seguintes atividades:Stemming das palavras,
                                    geração do TfidfVectorizer (12000 palavras)
                                    geração do DocumentTermMatrix
    """
    tfidf = TfidfVectorizer(stop_words=stopwords,
                            max_df=0.9, encoding='utf-8',
                            decode_error='ignore')
    if quer_stemming == 'True':
        st = Stemmer(language=linguagem)
        stemmed = st.fit_transform(df_column)
        base = tfidf.fit_transform(stemmed)
        data_dtm = pd.DataFrame(base.toarray(),
                                columns=tfidf.get_feature_names())
        data_dtm.index = df_column.index

    elif quer_stemming == 'False':
        base = tfidf.fit_transform(df_column)
        data_dtm = pd.DataFrame(base.toarray(),
                                columns=tfidf.get_feature_names())
        data_dtm.index = df_column.index

    return data_dtm, tfidf


data_dtm_en, tfidf_en = Gen_DocumentTermMatrix(corpus_en.texts,
                                               'english', stopwords,
                                               quer_stemming='True')
data_dtm_pt, tfidf_pt = Gen_DocumentTermMatrix(corpus_pt.texts,
                                               'portuguese', stopwords)

# =============================================================================
# English part
# =============================================================================
tdm_en = data_dtm_en.transpose()

sparse_counts_en = scipy.sparse.csr_matrix(tdm_en)
corpus_sp_en = matutils.Sparse2Corpus(sparse_counts_en)

id2word_en = dict((v, k) for k, v in tfidf_en.vocabulary_.items())

num_topics = 100
lda_en = LdaMulticore(corpus=corpus_sp_en, id2word=id2word_en,
                      num_topics=num_topics, passes=50, workers=3,
                      random_state=42, eta='auto',
                      chunksize=200, minimum_probability=0.0001)


# Dados usados no gráfico foram de:
# lda_en_first = LdaMulticore(corpus=corpus_sp_en, id2word=id2word_en,
#                       num_topics=num_topics, passes=50, workers=3,
#                       random_state=42)


# pickle.dump(lda_en, open(f'{local}\\lda_gensim\\lda_en(30topics).pkl', 'wb'))
# lda_en.save(f'{local}/lda_en30topics')


topicos_en = lda_en.get_document_topics(corpus_sp_en,
                                        minimum_probability=0.0)

docs_topic_en = pd.DataFrame()
dict_en = {}
indexes = []
for doc in range(len(topicos_en)):
    print(doc)
    index_docs = corpus_en.index.array[doc]
    indexes.append(index_docs)
    for i in topicos_en[doc]:
        index_topico, valor = i
        dict_en[index_topico] = valor
    df = pd.DataFrame(dict_en, index=indexes)
    docs_topic_en = docs_topic_en.append(df)
    indexes = []
    dict_en = {}

docs_topic_en.to_pickle(f'{local}//docs_topic_en({num_topics})v2.pkl')
# docs_topic_en.to_pickle(f'{local}//docs_topic_en(30).pkl')
# =============================================================================
# Portuguese
# =============================================================================

tdm_pt = data_dtm_pt.transpose()

sparse_counts_pt = scipy.sparse.csr_matrix(tdm_pt)
corpus_sp_pt = matutils.Sparse2Corpus(sparse_counts_pt)

id2word_pt = dict((v, k) for k, v in tfidf_pt.vocabulary_.items())

num_topics = 100
lda_pt = LdaMulticore(corpus=corpus_sp_pt, id2word=id2word_pt,
                      num_topics=num_topics, passes=30, workers=3,
                      random_state=42,
                      chunksize=200, minimum_probability=0.0001)
# pickle.dump(lda_en, open(f'{local}\\lda_gensim\\lda_pt(30topics).pkl', 'wb'))
# lda_pt.save(f'{local}/lda_gensim/lda_pt30topics')


topicos_pt = lda_pt.get_document_topics(corpus_sp_pt,
                                        minimum_probability=0.0)

docs_topic_pt = pd.DataFrame()
dict_pt = {}
indexes = []
for doc in range(len(topicos_pt)):
    print(doc)
    index_docs = corpus_pt.index.array[doc]
    indexes.append(index_docs)
    for i in topicos_pt[doc]:
        index_topico, valor = i
        dict_pt[index_topico] = valor
    df = pd.DataFrame(dict_pt, index=indexes)
    docs_topic_pt = docs_topic_pt.append(df)
    indexes = []
    dict_en = {}

docs_topic_pt.to_pickle(fr'{local}\docs_topic_pt({num_topics})v2.pkl')
mon = docs_topic_pt.to_numpy()
lda_pt.print_topics()
# docs_topic_pt.to_pickle(fr'{local}\docs_topic_pt(30).pkl')
# =============================================================================
# Test for model quality - Portuguese and english
# =============================================================================

d = corpora.Dictionary(corpus_pt.tokenized)
coerencia_model_pt = CoherenceModel(model=lda_pt,
                                    texts=corpus_pt.tokenized,
                                    dictionary=d,
                                    coherence='c_v')
coerencia_pt = coerencia_model_pt.get_coherence()

lda_en.print_topics()

e = corpora.Dictionary(corpus_en.tokenized)
coerencia_model_en = CoherenceModel(model=lda_en,
                                    texts=corpus_en.tokenized,
                                    dictionary=e,
                                    coherence='c_v')
coerencia_en = coerencia_model_en.get_coherence()


for doc in range(len(topicos_pt)):
    print(lda_pt[corpus_sp_pt[doc]])
