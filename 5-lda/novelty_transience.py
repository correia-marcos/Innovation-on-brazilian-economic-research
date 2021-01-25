# -*- coding: utf-8 -*-
"""
Script made to apply a Information Theory concept in the topic modelling base.

Kullback-leiber divergence was used to measure innovation, transience and
resonance in the production of articles approved for the annual meeting
of ANPEC.
It was measured in relation to each area that ANPEC used as a criterion between
2013 and 2019.

Article-based application: Individuals, Institutions, and Innovation in the
Debates of the French Revolution. The authors use LDA in a database
containing speeches made at the French national assembly to assess the KLD
as a measure of innovation and transience. There is a problem with our
application: the articles do not have a right order, except the year they were
published, that is, it is not possible to know the order in which articles
were approved in the same year.

To address this limitation, we decided to assess how each area of ​​research
(there are 13, according to anpec) developed innovation and transience as
follows way: the database was organized in order of year and was exchanged
n times of articles from the same year (in each simulation, one was positioned
in some random order) and a median of the result.

IMPORTANT: We made a relevant modification to the NTRexample_FRevNCa algorithm
to count the scale as all values ​​before the row
being analyzed.

IMPORANT2: The algorithm that determines the order of the articles of the
same year (in same area is random (randomly chooses the order) so that any
researcher wishing to run this script will have slightly
about novelty, transience and innovation. It is argued that
values ​​become asymptotically close if the det_KLD_random function is
round n times with n ~ ∞ (law of large numbers).

"""
import os
import pandas as pd
import logging
os.chdir('C:\\Users\\Usuário\\Projects\\monografia\\5-lda')
from NTRexample_FRevNCA import calculate_novelty_transience_resonance as cntr

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.INFO)


def mysplit3(s) -> str:
    """Do a simple split of numbers and ."""
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

df = df.drop('tí­tulo', 1)
df = df.drop('docs', 1)
df = df.drop('autores_universi.', 1)


# docs_topic_en = pd.read_pickle(f'{local}/docs_topic_en(30).pkl')
# docs_topic_pt = pd.read_pickle(f'{local}/docs_topic_pt(30).pkl')


docs_topic_en = pd.read_pickle(f'{local}/docs_topic_en(30)v2.pkl')
docs_topic_pt = pd.read_pickle(f'{local}/docs_topic_pt(30)v2.pkl')


groups = df.groupby(['linguagem', 'code_area', 'ano'])
groups.groups
dfs = dict(tuple(groups))

dfs.pop(('es', 'i06', '2014'))
dfs.pop(('es', 'i02', '2014'))


def get_KLD_random_ano():
    """Segments the calculation of novelty (and the others) by area and year.

    The most important aspect is that this function randomizes the entries of
    the same year.
    """
    lista_frames_ena2013 = []
    lista_frames_ena2014 = []
    lista_frames_ena2015 = []
    lista_frames_ena2016 = []
    lista_frames_ena2017 = []
    lista_frames_ena2018 = []
    lista_frames_ena2019 = []
    lista_frames_pta2013 = []
    lista_frames_pta2014 = []
    lista_frames_pta2015 = []
    lista_frames_pta2016 = []
    lista_frames_pta2017 = []
    lista_frames_pta2018 = []
    lista_frames_pta2019 = []
    frame1 = pd.DataFrame()
    frame2 = pd.DataFrame()
    frame3 = pd.DataFrame()
    frame4 = pd.DataFrame()
    frame5 = pd.DataFrame()
    frame6 = pd.DataFrame()
    frame7 = pd.DataFrame()
    frame8 = pd.DataFrame()
    frame9 = pd.DataFrame()
    frame10 = pd.DataFrame()
    frame11 = pd.DataFrame()
    frame12 = pd.DataFrame()
    frame13 = pd.DataFrame()
    frame14 = pd.DataFrame()

    for keys in dfs:
        lingua, area, ano = keys
        if lingua == 'en':
            if ano == '2013':
                dfs[keys] = dfs[keys].sample(frac=1)
                kld_topics_en = pd.DataFrame(docs_topic_en[
                    docs_topic_en.index.isin(dfs[keys].index)],
                                             index=dfs[keys].index)
                frame1 = frame1.append(kld_topics_en)
                frame1 = frame1.sample(frac=1)
                lista_frames_ena2013.append(frame1)

            elif ano == '2014':
                dfs[keys] = dfs[keys].sample(frac=1)
                kld_topics_en = pd.DataFrame(docs_topic_en[
                    docs_topic_en.index.isin(dfs[keys].index)],
                                             index=dfs[keys].index)
                frame2 = frame2.append(kld_topics_en)
                frame2 = frame2.sample(frac=1)
                lista_frames_ena2014.append(frame2)

            elif ano == '2015':
                dfs[keys] = dfs[keys].sample(frac=1)
                kld_topics_en = pd.DataFrame(docs_topic_en[
                    docs_topic_en.index.isin(dfs[keys].index)],
                                             index=dfs[keys].index)
                frame3 = frame3.append(kld_topics_en)
                frame3 = frame3.sample(frac=1)
                lista_frames_ena2015.append(frame3)

            elif ano == '2016':
                dfs[keys] = dfs[keys].sample(frac=1)
                kld_topics_en = pd.DataFrame(docs_topic_en[
                    docs_topic_en.index.isin(dfs[keys].index)],
                                             index=dfs[keys].index)
                frame4 = frame4.append(kld_topics_en)
                frame4 = frame4.sample(frac=1)
                lista_frames_ena2016.append(frame4)

            elif ano == '2017':
                dfs[keys] = dfs[keys].sample(frac=1)
                kld_topics_en = pd.DataFrame(docs_topic_en[
                    docs_topic_en.index.isin(dfs[keys].index)],
                                             index=dfs[keys].index)
                frame5 = frame5.append(kld_topics_en)
                frame5 = frame5.sample(frac=1)
                lista_frames_ena2017.append(frame5)

            elif ano == '2018':
                dfs[keys] = dfs[keys].sample(frac=1)
                kld_topics_en = pd.DataFrame(docs_topic_en[
                    docs_topic_en.index.isin(dfs[keys].index)],
                                             index=dfs[keys].index)
                frame6 = frame6.append(kld_topics_en)
                frame6 = frame6.sample(frac=1)
                lista_frames_ena2018.append(frame6)

            elif ano == '2019':
                dfs[keys] = dfs[keys].sample(frac=1)
                kld_topics_en = pd.DataFrame(docs_topic_en[
                    docs_topic_en.index.isin(dfs[keys].index)],
                                             index=dfs[keys].index)
                frame7 = frame7.append(kld_topics_en)
                frame7 = frame7.sample(frac=1)
                lista_frames_ena2019.append(frame7)

        if lingua == 'pt':
            if ano == '2013':
                dfs[keys] = dfs[keys].sample(frac=1)
                kld_topics_pt = pd.DataFrame(docs_topic_pt[
                    docs_topic_pt.index.isin(dfs[keys].index)],
                                             index=dfs[keys].index)
                frame8 = frame8.append(kld_topics_pt)
                frame8 = frame8.sample(frac=1)
                lista_frames_pta2013.append(frame8)

            elif ano == '2014':
                dfs[keys] = dfs[keys].sample(frac=1)
                kld_topics_pt = pd.DataFrame(docs_topic_pt[
                    docs_topic_pt.index.isin(dfs[keys].index)],
                                             index=dfs[keys].index)
                frame9 = frame9.append(kld_topics_pt)
                frame9 = frame9.sample(frac=1)
                lista_frames_pta2014.append(frame9)

            elif ano == '2015':
                dfs[keys] = dfs[keys].sample(frac=1)
                kld_topics_pt = pd.DataFrame(docs_topic_pt[
                    docs_topic_pt.index.isin(dfs[keys].index)],
                                             index=dfs[keys].index)
                frame10 = frame10.append(kld_topics_pt)
                frame10 = frame10.sample(frac=1)
                lista_frames_pta2015.append(frame10)

            elif ano == '2016':
                dfs[keys] = dfs[keys].sample(frac=1)
                kld_topics_pt = pd.DataFrame(docs_topic_pt[
                    docs_topic_pt.index.isin(dfs[keys].index)],
                                             index=dfs[keys].index)
                frame11 = frame11.append(kld_topics_pt)
                frame11 = frame11.sample(frac=1)
                lista_frames_pta2016.append(frame11)

            elif ano == '2017':
                dfs[keys] = dfs[keys].sample(frac=1)
                kld_topics_pt = pd.DataFrame(docs_topic_pt[
                    docs_topic_pt.index.isin(dfs[keys].index)],
                                             index=dfs[keys].index)
                frame12 = frame12.append(kld_topics_pt)
                frame12 = frame12.sample(frac=1)
                lista_frames_pta2017.append(frame12)

            elif ano == '2018':
                dfs[keys] = dfs[keys].sample(frac=1)
                kld_topics_pt = pd.DataFrame(docs_topic_pt[
                    docs_topic_pt.index.isin(dfs[keys].index)],
                                             index=dfs[keys].index)
                frame13 = frame13.append(kld_topics_pt)
                frame13 = frame13.sample(frac=1)
                lista_frames_pta2018.append(frame13)

            elif ano == '2019':
                dfs[keys] = dfs[keys].sample(frac=1)
                kld_topics_pt = pd.DataFrame(docs_topic_pt[
                    docs_topic_pt.index.isin(dfs[keys].index)],
                                             index=dfs[keys].index)
                frame14 = frame14.append(kld_topics_pt)
                frame14 = frame14.sample(frac=1)
                lista_frames_pta2019.append(frame14)

    dfinal_en = pd.DataFrame()
    dfinal_pt = pd.DataFrame()
    dfinal_en = dfinal_en.append([lista_frames_ena2013[-1],
                                  lista_frames_ena2014[-1],
                                  lista_frames_ena2015[-1],
                                  lista_frames_ena2016[-1],
                                  lista_frames_ena2017[-1],
                                  lista_frames_ena2018[-1],
                                  lista_frames_ena2019[-1]])

    dfinal_pt = dfinal_pt.append([lista_frames_pta2013[-1],
                                  lista_frames_pta2014[-1],
                                  lista_frames_pta2015[-1],
                                  lista_frames_pta2016[-1],
                                  lista_frames_pta2017[-1],
                                  lista_frames_pta2018[-1],
                                  lista_frames_pta2019[-1]])

    novelties_en, transiences_en, ressonances_en = \
        cntr.nov_tran_reson_no_scale(dfinal_en)

    novelties_pt, transiences_pt, ressonances_pt = \
        cntr.nov_tran_reson_no_scale(dfinal_pt)

    frame_en = pd.DataFrame({'novelties': novelties_en,
                             'transiences': transiences_en,
                             'ressonances': ressonances_en},
                            index=dfinal_en.index)

    frame_pt = pd.DataFrame({'novelties': novelties_pt,
                             'transiences': transiences_pt,
                             'ressonances': ressonances_pt},
                            index=dfinal_pt.index)
    dfinal = pd.concat([frame_en, frame_pt])
    dfinal = dfinal.sort_index()

    return dfinal


def get_KLD_random_area():
    """Segments the calculation of novelty (e the others 2) for area and year.

    Most important aspect is that this function randomizes the entries of the
    same year e same area.
    """
    lista_frames_ena1 = []
    lista_frames_ena2 = []
    lista_frames_ena3 = []
    lista_frames_ena4 = []
    lista_frames_ena5 = []
    lista_frames_ena6 = []
    lista_frames_ena7 = []
    lista_frames_ena8 = []
    lista_frames_ena9 = []
    lista_frames_ena10 = []
    lista_frames_ena11 = []
    lista_frames_ena12 = []
    lista_frames_ena13 = []
    lista_frames_pta1 = []
    lista_frames_pta2 = []
    lista_frames_pta3 = []
    lista_frames_pta4 = []
    lista_frames_pta5 = []
    lista_frames_pta6 = []
    lista_frames_pta7 = []
    lista_frames_pta8 = []
    lista_frames_pta9 = []
    lista_frames_pta10 = []
    lista_frames_pta11 = []
    lista_frames_pta12 = []
    lista_frames_pta13 = []
    frame1 = pd.DataFrame()
    frame2 = pd.DataFrame()
    frame3 = pd.DataFrame()
    frame4 = pd.DataFrame()
    frame5 = pd.DataFrame()
    frame6 = pd.DataFrame()
    frame7 = pd.DataFrame()
    frame8 = pd.DataFrame()
    frame9 = pd.DataFrame()
    frame10 = pd.DataFrame()
    frame11 = pd.DataFrame()
    frame12 = pd.DataFrame()
    frame13 = pd.DataFrame()
    frame14 = pd.DataFrame()
    frame15 = pd.DataFrame()
    frame16 = pd.DataFrame()
    frame17 = pd.DataFrame()
    frame18 = pd.DataFrame()
    frame19 = pd.DataFrame()
    frame20 = pd.DataFrame()
    frame21 = pd.DataFrame()
    frame22 = pd.DataFrame()
    frame23 = pd.DataFrame()
    frame24 = pd.DataFrame()
    frame25 = pd.DataFrame()
    frame26 = pd.DataFrame()

    for keys in dfs:
        lingua, area, ano = keys
        if lingua == 'en':
            if area == 'i01':
                # for i in range(5):
                dfs[keys] = dfs[keys].sample(frac=1)
                kld_topics_en = pd.DataFrame(docs_topic_en[
                    docs_topic_en.index.isin(dfs[keys].index)],
                                             index=dfs[keys].index)
                frame1 = frame1.append(kld_topics_en)
                novelties, transiences, ressonances =  \
                    cntr.nov_tran_reson_no_scale(frame1)
                frame_df = pd.DataFrame({'novelties': novelties,
                                         'transiences': transiences,
                                         'ressonances': ressonances},
                                        index=frame1.index)
                lista_frames_ena1.append(frame_df)

            elif area == 'i02':
                dfs[keys] = dfs[keys].sample(frac=1)
                kld_topics_en = pd.DataFrame(docs_topic_en[
                    docs_topic_en.index.isin(dfs[keys].index)],
                                             index=dfs[keys].index)
                frame2 = frame2.append(kld_topics_en)
                novelties, transiences, ressonances =  \
                    cntr.nov_tran_reson_no_scale(frame2)
                frame_df = pd.DataFrame({'novelties': novelties,
                                         'transiences': transiences,
                                         'ressonances': ressonances},
                                        index=frame2.index)
                lista_frames_ena2.append(frame_df)

            elif area == 'i03':
                dfs[keys] = dfs[keys].sample(frac=1)
                kld_topics_en = pd.DataFrame(docs_topic_en[
                    docs_topic_en.index.isin(dfs[keys].index)],
                                             index=dfs[keys].index)
                frame3 = frame3.append(kld_topics_en)
                novelties, transiences, ressonances =  \
                    cntr.nov_tran_reson_no_scale(frame3)
                frame_df = pd.DataFrame({'novelties': novelties,
                                         'transiences': transiences,
                                         'ressonances': ressonances},
                                        index=frame3.index)
                lista_frames_ena3.append(frame_df)

            elif area == 'i04':
                dfs[keys] = dfs[keys].sample(frac=1)
                kld_topics_en = pd.DataFrame(docs_topic_en[
                    docs_topic_en.index.isin(dfs[keys].index)],
                                             index=dfs[keys].index)
                frame4 = frame4.append(kld_topics_en)
                novelties, transiences, ressonances =  \
                    cntr.nov_tran_reson_no_scale(frame4)
                frame_df = pd.DataFrame({'novelties': novelties,
                                         'transiences': transiences,
                                         'ressonances': ressonances},
                                        index=frame4.index)
                lista_frames_ena4.append(frame_df)

            elif area == 'i05':
                dfs[keys] = dfs[keys].sample(frac=1)
                kld_topics_en = pd.DataFrame(docs_topic_en[
                    docs_topic_en.index.isin(dfs[keys].index)],
                                             index=dfs[keys].index)
                frame5 = frame5.append(kld_topics_en)
                novelties, transiences, ressonances =  \
                    cntr.nov_tran_reson_no_scale(frame5)
                frame_df = pd.DataFrame({'novelties': novelties,
                                         'transiences': transiences,
                                         'ressonances': ressonances},
                                        index=frame5.index)
                lista_frames_ena5.append(frame_df)

            elif area == 'i06':
                dfs[keys] = dfs[keys].sample(frac=1)
                kld_topics_en = pd.DataFrame(docs_topic_en[
                    docs_topic_en.index.isin(dfs[keys].index)],
                                             index=dfs[keys].index)
                frame6 = frame6.append(kld_topics_en)
                novelties, transiences, ressonances =  \
                    cntr.nov_tran_reson_no_scale(frame6)
                frame_df = pd.DataFrame({'novelties': novelties,
                                         'transiences': transiences,
                                         'ressonances': ressonances},
                                        index=frame6.index)
                lista_frames_ena6.append(frame_df)

            elif area == 'i07':
                dfs[keys] = dfs[keys].sample(frac=1)
                kld_topics_en = pd.DataFrame(docs_topic_en[
                    docs_topic_en.index.isin(dfs[keys].index)],
                                             index=dfs[keys].index)
                frame7 = frame7.append(kld_topics_en)
                novelties, transiences, ressonances =  \
                    cntr.nov_tran_reson_no_scale(frame7)
                frame_df = pd.DataFrame({'novelties': novelties,
                                         'transiences': transiences,
                                         'ressonances': ressonances},
                                        index=frame7.index)
                lista_frames_ena7.append(frame_df)

            elif area == 'i08':
                dfs[keys] = dfs[keys].sample(frac=1)
                kld_topics_en = pd.DataFrame(docs_topic_en[
                    docs_topic_en.index.isin(dfs[keys].index)],
                                             index=dfs[keys].index)
                frame8 = frame8.append(kld_topics_en)
                novelties, transiences, ressonances =  \
                    cntr.nov_tran_reson_no_scale(frame8)
                frame_df = pd.DataFrame({'novelties': novelties,
                                         'transiences': transiences,
                                         'ressonances': ressonances},
                                        index=frame8.index)
                lista_frames_ena8.append(frame_df)

            elif area == 'i09':
                dfs[keys] = dfs[keys].sample(frac=1)
                kld_topics_en = pd.DataFrame(docs_topic_en[
                    docs_topic_en.index.isin(dfs[keys].index)],
                                             index=dfs[keys].index)
                frame9 = frame9.append(kld_topics_en)
                novelties, transiences, ressonances =  \
                    cntr.nov_tran_reson_no_scale(frame9)
                frame_df = pd.DataFrame({'novelties': novelties,
                                         'transiences': transiences,
                                         'ressonances': ressonances},
                                        index=frame9.index)
                lista_frames_ena9.append(frame_df)

            elif area == 'i10':
                dfs[keys] = dfs[keys].sample(frac=1)
                kld_topics_en = pd.DataFrame(docs_topic_en[
                    docs_topic_en.index.isin(dfs[keys].index)],
                                             index=dfs[keys].index)
                frame10 = frame10.append(kld_topics_en)
                novelties, transiences, ressonances =  \
                    cntr.nov_tran_reson_no_scale(frame10)
                frame_df = pd.DataFrame({'novelties': novelties,
                                         'transiences': transiences,
                                         'ressonances': ressonances},
                                        index=frame10.index)
                lista_frames_ena10.append(frame_df)

            elif area == 'i11':
                dfs[keys] = dfs[keys].sample(frac=1)
                kld_topics_en = pd.DataFrame(docs_topic_en[
                    docs_topic_en.index.isin(dfs[keys].index)],
                                             index=dfs[keys].index)
                frame11 = frame11.append(kld_topics_en)
                novelties, transiences, ressonances =  \
                    cntr.nov_tran_reson_no_scale(frame11)
                frame_df = pd.DataFrame({'novelties': novelties,
                                         'transiences': transiences,
                                         'ressonances': ressonances},
                                        index=frame11.index)
                lista_frames_ena11.append(frame_df)

            elif area == 'i12':
                dfs[keys] = dfs[keys].sample(frac=1)
                kld_topics_en = pd.DataFrame(docs_topic_en[
                    docs_topic_en.index.isin(dfs[keys].index)],
                                             index=dfs[keys].index)
                frame12 = frame12.append(kld_topics_en)
                novelties, transiences, ressonances =  \
                    cntr.nov_tran_reson_no_scale(frame12)
                frame_df = pd.DataFrame({'novelties': novelties,
                                         'transiences': transiences,
                                         'ressonances': ressonances},
                                        index=frame12.index)
                lista_frames_ena12.append(frame_df)

            elif area == 'i13':
                dfs[keys] = dfs[keys].sample(frac=1)
                kld_topics_en = pd.DataFrame(docs_topic_en[
                    docs_topic_en.index.isin(dfs[keys].index)],
                                             index=dfs[keys].index)
                frame13 = frame13.append(kld_topics_en)
                novelties, transiences, ressonances =  \
                    cntr.nov_tran_reson_no_scale(frame13)
                frame_df = pd.DataFrame({'novelties': novelties,
                                         'transiences': transiences,
                                         'ressonances': ressonances},
                                        index=frame13.index)
                lista_frames_ena13.append(frame_df)

        if lingua == 'pt':
            if area == 'i01':
                # for i in range(5):
                dfs[keys] = dfs[keys].sample(frac=1)
                kld_topics_pt = pd.DataFrame(docs_topic_pt[
                    docs_topic_pt.index.isin(dfs[keys].index)],
                                             index=dfs[keys].index)
                frame14 = frame14.append(kld_topics_pt)
                novelties, transiences, ressonances =  \
                    cntr.nov_tran_reson_no_scale(frame14)
                frame_df = pd.DataFrame({'novelties': novelties,
                                         'transiences': transiences,
                                         'ressonances': ressonances},
                                        index=frame14.index)
                lista_frames_pta1.append(frame_df)

            elif area == 'i02':
                dfs[keys] = dfs[keys].sample(frac=1)
                kld_topics_pt = pd.DataFrame(docs_topic_pt[
                    docs_topic_pt.index.isin(dfs[keys].index)],
                                             index=dfs[keys].index)
                frame15 = frame15.append(kld_topics_pt)
                novelties, transiences, ressonances =  \
                    cntr.nov_tran_reson_no_scale(frame15)
                frame_df = pd.DataFrame({'novelties': novelties,
                                         'transiences': transiences,
                                         'ressonances': ressonances},
                                        index=frame15.index)
                lista_frames_pta2.append(frame_df)

            elif area == 'i03':
                dfs[keys] = dfs[keys].sample(frac=1)
                kld_topics_pt = pd.DataFrame(docs_topic_pt[
                    docs_topic_pt.index.isin(dfs[keys].index)],
                                             index=dfs[keys].index)
                frame16 = frame16.append(kld_topics_pt)
                novelties, transiences, ressonances =  \
                    cntr.nov_tran_reson_no_scale(frame16)
                frame_df = pd.DataFrame({'novelties': novelties,
                                         'transiences': transiences,
                                         'ressonances': ressonances},
                                        index=frame16.index)
                lista_frames_pta3.append(frame_df)

            elif area == 'i04':
                dfs[keys] = dfs[keys].sample(frac=1)
                kld_topics_pt = pd.DataFrame(docs_topic_pt[
                    docs_topic_pt.index.isin(dfs[keys].index)],
                                             index=dfs[keys].index)
                frame17 = frame17.append(kld_topics_pt)
                novelties, transiences, ressonances =  \
                    cntr.nov_tran_reson_no_scale(frame17)
                frame_df = pd.DataFrame({'novelties': novelties,
                                         'transiences': transiences,
                                         'ressonances': ressonances},
                                        index=frame17.index)
                lista_frames_pta4.append(frame_df)

            elif area == 'i05':
                dfs[keys] = dfs[keys].sample(frac=1)
                kld_topics_pt = pd.DataFrame(docs_topic_pt[
                    docs_topic_pt.index.isin(dfs[keys].index)],
                                             index=dfs[keys].index)
                frame18 = frame18.append(kld_topics_pt)
                novelties, transiences, ressonances =  \
                    cntr.nov_tran_reson_no_scale(frame18)
                frame_df = pd.DataFrame({'novelties': novelties,
                                         'transiences': transiences,
                                         'ressonances': ressonances},
                                        index=frame18.index)
                lista_frames_pta5.append(frame_df)

            elif area == 'i06':
                dfs[keys] = dfs[keys].sample(frac=1)
                kld_topics_pt = pd.DataFrame(docs_topic_pt[
                    docs_topic_pt.index.isin(dfs[keys].index)],
                                             index=dfs[keys].index)
                frame19 = frame19.append(kld_topics_pt)
                novelties, transiences, ressonances =  \
                    cntr.nov_tran_reson_no_scale(frame19)
                frame_df = pd.DataFrame({'novelties': novelties,
                                         'transiences': transiences,
                                         'ressonances': ressonances},
                                        index=frame19.index)
                lista_frames_pta6.append(frame_df)

            elif area == 'i07':
                dfs[keys] = dfs[keys].sample(frac=1)
                kld_topics_pt = pd.DataFrame(docs_topic_pt[
                    docs_topic_pt.index.isin(dfs[keys].index)],
                                             index=dfs[keys].index)
                frame20 = frame20.append(kld_topics_pt)
                novelties, transiences, ressonances =  \
                    cntr.nov_tran_reson_no_scale(frame20)
                frame_df = pd.DataFrame({'novelties': novelties,
                                         'transiences': transiences,
                                         'ressonances': ressonances},
                                        index=frame20.index)
                lista_frames_pta7.append(frame_df)

            elif area == 'i08':
                dfs[keys] = dfs[keys].sample(frac=1)
                kld_topics_pt = pd.DataFrame(docs_topic_pt[
                    docs_topic_pt.index.isin(dfs[keys].index)],
                                             index=dfs[keys].index)
                frame21 = frame21.append(kld_topics_pt)
                novelties, transiences, ressonances =  \
                    cntr.nov_tran_reson_no_scale(frame21)
                frame_df = pd.DataFrame({'novelties': novelties,
                                         'transiences': transiences,
                                         'ressonances': ressonances},
                                        index=frame21.index)
                lista_frames_pta8.append(frame_df)

            elif area == 'i09':
                dfs[keys] = dfs[keys].sample(frac=1)
                kld_topics_pt = pd.DataFrame(docs_topic_pt[
                    docs_topic_pt.index.isin(dfs[keys].index)],
                                             index=dfs[keys].index)
                frame22 = frame22.append(kld_topics_pt)
                novelties, transiences, ressonances =  \
                    cntr.nov_tran_reson_no_scale(frame22)
                frame_df = pd.DataFrame({'novelties': novelties,
                                         'transiences': transiences,
                                         'ressonances': ressonances},
                                        index=frame22.index)
                lista_frames_pta9.append(frame_df)

            elif area == 'i10':
                dfs[keys] = dfs[keys].sample(frac=1)
                kld_topics_pt = pd.DataFrame(docs_topic_pt[
                    docs_topic_pt.index.isin(dfs[keys].index)],
                                             index=dfs[keys].index)
                frame23 = frame23.append(kld_topics_pt)
                novelties, transiences, ressonances =  \
                    cntr.nov_tran_reson_no_scale(frame23)
                frame_df = pd.DataFrame({'novelties': novelties,
                                         'transiences': transiences,
                                         'ressonances': ressonances},
                                        index=frame23.index)
                lista_frames_pta10.append(frame_df)

            elif area == 'i11':
                dfs[keys] = dfs[keys].sample(frac=1)
                kld_topics_pt = pd.DataFrame(docs_topic_pt[
                    docs_topic_pt.index.isin(dfs[keys].index)],
                                             index=dfs[keys].index)
                frame24 = frame24.append(kld_topics_pt)
                novelties, transiences, ressonances =  \
                    cntr.nov_tran_reson_no_scale(frame24)
                frame_df = pd.DataFrame({'novelties': novelties,
                                         'transiences': transiences,
                                         'ressonances': ressonances},
                                        index=frame24.index)
                lista_frames_pta11.append(frame_df)

            elif area == 'i12':
                dfs[keys] = dfs[keys].sample(frac=1)
                kld_topics_pt = pd.DataFrame(docs_topic_pt[
                    docs_topic_pt.index.isin(dfs[keys].index)],
                                             index=dfs[keys].index)
                frame25 = frame25.append(kld_topics_pt)
                novelties, transiences, ressonances =  \
                    cntr.nov_tran_reson_no_scale(frame25)
                frame_df = pd.DataFrame({'novelties': novelties,
                                         'transiences': transiences,
                                         'ressonances': ressonances},
                                        index=frame25.index)
                lista_frames_pta12.append(frame_df)

            elif area == 'i13':
                dfs[keys] = dfs[keys].sample(frac=1)
                kld_topics_pt = pd.DataFrame(docs_topic_pt[
                    docs_topic_pt.index.isin(dfs[keys].index)],
                                             index=dfs[keys].index)
                frame26 = frame26.append(kld_topics_pt)
                novelties, transiences, ressonances =  \
                    cntr.nov_tran_reson_no_scale(frame26)
                frame_df = pd.DataFrame({'novelties': novelties,
                                         'transiences': transiences,
                                         'ressonances': ressonances},
                                        index=frame26.index)
                lista_frames_pta13.append(frame_df)
    dfinal = pd.DataFrame()
    dfinal = dfinal.append([lista_frames_ena1[-1], lista_frames_ena2[-1],
                           lista_frames_ena3[-1], lista_frames_ena4[-1],
                           lista_frames_ena5[-1], lista_frames_ena6[-1],
                           lista_frames_ena7[-1], lista_frames_ena8[-1],
                           lista_frames_ena9[-1], lista_frames_ena10[-1],
                           lista_frames_ena11[-1], lista_frames_ena12[-1],
                           lista_frames_ena13[-1], lista_frames_pta1[-1],
                           lista_frames_pta2[-1], lista_frames_pta3[-1],
                           lista_frames_pta4[-1], lista_frames_pta5[-1],
                           lista_frames_pta6[-1], lista_frames_pta7[-1],
                           lista_frames_pta8[-1], lista_frames_pta9[-1],
                           lista_frames_pta10[-1], lista_frames_pta11[-1],
                           lista_frames_pta12[-1], lista_frames_pta13[-1]])
    dfinal = dfinal.sort_index()

    return dfinal


def rodar_KLD_random_nvezes(n, tipo='area'):
    """
    Take the previous function, run it n times and generate a median.

    Take the previous function, run it n times and generate a median value
    for each item.
    """
    lista_df_KLDs = []
    if tipo == 'area':
        for i in range(n):
            Kld = get_KLD_random_area()
            lista_df_KLDs.append(Kld)
    elif tipo == 'ano':
        for i in range(n):
            Kld = get_KLD_random_ano()
            lista_df_KLDs.append(Kld)
    else:
        raise ValueError('Só pode ser os tipos: "area" ou "ano"')
        pass
    df_concat = pd.concat((i for i in lista_df_KLDs))
    by_row_index = df_concat.groupby(df_concat.index)
    df_median = by_row_index.median()

    return df_median


# Change the "local" variable below
local = 'C:\\Users\\Usuário\\Projects\\monografia\\dados\\data_final'
# base1 = rodar_KLD_random_nvezes(40, 'area')
# base1.to_pickle(f'{local}/data_KLD.pkl')
# base2 = rodar_KLD_random_nvezes(50, 'ano')
# base2.to_pickle(f'{local}/data_KLDv2.pkl')
NTR_df = rodar_KLD_random_nvezes(50, 'area')
NTR_df.to_pickle(f'{local}/data_KLDv3.pkl')

# =============================================================================
# Parte final
# =============================================================================
df = pd.concat([corpus, data], axis=1, sort=False)
df = df[df.texts.notna()]
df['docs'] = df.index
df['ano'] = df.docs.str.split('_')
df.loc[:, 'ano'] = df.ano.map(lambda x: x[1])
df = df.drop('docs', 1)

mean_std_geral = NTR_df.agg(['mean', 'std'])
mean_std_geral.to_excel(f'{local}/NTR_mean_std_geral.xlsx')

NTR_df['área'] = df.code_area
NTR_df_grouped = NTR_df.groupby(NTR_df.área)
NTR_df_mean_std = NTR_df_grouped.agg(['mean', 'std'])
NTR_df_mean_std.to_pickle(f'{local}/NTR_média+std_area.pkl')
NTR_df_mean_std.to_excel(f'{local}/NTR_média+std_area.xlsx',
                         encoding='utf-8')

NTR_df['título'] = df['tí­tulo']
NTR_df['Nome_Área'] = df['Área']
NTR_df['autores'] = df['autores_universi.']
extremos = NTR_df.nsmallest(5, 'novelties')
extremos = extremos.append(NTR_df.nlargest(5, 'novelties'))
extremos.to_excel(f'{local}/maiores_menores_NTR.xlsx', encoding='utf-8')

# NTR_df_mean_std = pd.read_csv(f'{local}/NTR_média+std_area.csv')
