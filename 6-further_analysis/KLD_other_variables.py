"""
This script was made to anaylse the relation. between and novelty and citation.

Other relations were analysed as well.
Ressonance is from 5-lda scripts (novelty, transience, ressonance).

VERY IMPORTANT: The citation database was partly created out of this python
project.
We googled the paper and save the quantity of citation in a excel file that
is now located on "dados" file.
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


root = os.path.abspath(os.curdir)
local_final = r'dados/data_final'

# =============================================================================
# First treatment of databases
# =============================================================================

kld = pd.read_pickle(f'{root}/{local_final}/data_KLDv4(30_gensim).pkl')
data = pd.read_pickle(f'{root}/{local_final}/data_final_v2.pkl')

data['docs'] = data.index
data['ano'] = data.docs.str.split('_')
data.loc[:, 'ano'] = data.ano.map(lambda x: x[1])
data = data.drop('docs', 1)


xls = pd.ExcelFile(f'{root}/dados/outside/citations.xlsx')
citations_base = pd.read_excel(xls, 'base', index_col='doc_num')


citations_base['docs'] = citations_base.index
citations_base['ano'] = citations_base.docs.str.split('_')
citations_base.loc[:, 'ano'] = citations_base.ano.map(lambda x: x[1])
citations_base = citations_base.drop('docs', 1)
citations_base = citations_base.drop('doc', 1)

cols = citations_base.columns.to_list()
cols = cols[0:6] + cols[-1:] + cols[6:-1]
citations_base = citations_base[cols]

citations_base['code_area'] = data.code_area

cols = citations_base.columns.to_list()
cols = cols[0:4] + cols[-1:] + cols[4:10]
df = citations_base[cols]

del cols


df = df[~df.index.duplicated(keep='first')]

df_merge = pd.merge(kld, df[['citations', 'num-authors', 'code_area',
                             'ano']],
                    left_index=True,
                    right_index=True).drop_duplicates()

# =============================================================================
# Plot for citations x ressonance
# =============================================================================

quantil_citations = df_merge.citations.quantile(0.7)
quantil_ressonances = df_merge.ressonances.quantile(0.7)

mean_citations = df_merge.citations.mean()
mean_ressonances = df_merge.ressonances.mean()


df_maior = df_merge[(df_merge.ressonances > quantil_ressonances) &
                    (df_merge.citations > quantil_citations)]

sns.scatterplot(data=df_maior, x='ressonances', y='citations',
                hue='num-authors')
# =============================================================================
# plot for area
# =============================================================================

group_area = df_merge.groupby('code_area')
test = dict(tuple(group_area))
df_area = group_area.agg('median')
mean_area_novelty = df_area.novelties.mean()
mean_area_ressonance = df_area.ressonances.mean()


sns.scatterplot(data=df_area, x='novelties', y='ressonances',
                hue=df_area.index, palette='flare')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.axvline(mean_area_novelty, color='black')
plt.axhline(mean_area_ressonance, color='black')
plt.show()


# =============================================================================
# Plot for num-author in time
# =============================================================================
df_authors = df_merge[['num-authors', 'ano']]
df_author_melt = pd.melt(df_authors, ['ano'])

df_author_gb = df_authors.groupby('ano').agg('mean')

sns.lineplot(data=df_author_gb, x='ano', y='num-authors')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2,
           borderaxespad=0.)
plt.show()

# =============================================================================
# Plot novelty vs ressonance
# =============================================================================

sns.scatterplot(data=df_merge, x='novelties', y='ressonances',
                hue='num-authors')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.show()

# =============================================================================
# Correlations
# =============================================================================

corr_transience_citations = df.citations.corr(df.ressonances)
corr_novelty_citations = df.citations.corr(df.novelties)

corr_novelty_transience = df.ressonances.corr(df.novelties)

corr_transience_authors = df.tra

correlations = df_merge.corr()
correlations.to_excel(f'{root}/dados/outside/correlation.xlsx')
