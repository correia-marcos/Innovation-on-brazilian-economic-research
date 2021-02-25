"""
This script was made to anaylse the relation. between and novelty and depts.

Ressonance is from 5-lda scripts (novelty, transience, ressonance).

VERY IMPORTANT: In papers where two or more coautors are from the same
university we counted repeated the line for the calculations purpose.
Example: paper 'x' with coautors from: unb, unb and ufpa.
--> we counted unb twice!

IMPORTANT: The citation database was partly created out of this python
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
depts_base = pd.read_excel(xls, 'size', index_col='ANPEC')
depts_base.drop_duplicates()

citations_base['docs'] = citations_base.index
citations_base['ano'] = citations_base.docs.str.split('_')
citations_base.loc[:, 'ano'] = citations_base.ano.map(lambda x: x[1])
citations_base = citations_base.drop('docs', 1)
citations_base = citations_base.drop('doc', 1)

cols = citations_base.columns.to_list()
cols = cols[0:6] + cols[-1:] + cols[6:-1]
citations_base = citations_base[cols]

citations_base['code_area'] = data.code_area

# =============================================================================
# FInal dataset
# =============================================================================

df_merge = pd.merge(kld, citations_base[['citations', 'Dept', 'num-authors']],
                    left_index=True,
                    right_index=True)
df_merge.Dept = df_merge.Dept.str.strip()

data_depts_grouped = df_merge.groupby('Dept')

data_depts = data_depts_grouped.agg('mean')
data_depts['quantidade_artigos'] = data_depts_grouped.size()
data_depts['mean_ressonances'] = data_depts.ressonances.mean()

data_depts = data_depts.sort_values('ressonances', ascending=False)

data_depts.to_excel(f'{root}/dados/outside/depts_kld.xlsx')

# =============================================================================
# Plots
# =============================================================================
depts_allowed = depts_base[depts_base.is_member == 1]

data_depts['member'] = depts_allowed.is_member
base = data_depts[data_depts.member == 1]

mean_depts_novelty = data_depts.novelties.mean()
mean_depts_ressonance = data_depts.ressonances.mean()

data_depts['depts'] = data_depts.index
data_depts.columns = ['novelty', 'transience', 'ressonance', 'citations',
                      'num-authors', 'quantidade_artigos', 'mean_ressonances',
                      'member', 'depts']

base['depts'] = base.index
base.columns = ['novelty', 'transience', 'ressonance', 'citations',
                'num-authors', 'amount_papers', 'mean_ressonances',
                'member', 'depts']

plot1 = sns.scatterplot(data=base, x='novelty', y='ressonance',
                        size='amount_papers', sizes=(50, 200))
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.axvline(mean_depts_novelty, color='gray')
plt.axhline(mean_depts_ressonance, color='gray')


# for line in range(base.shape[0]):
#     plot1.text(base.novelty[line]+0.05, base.ressonance[line],
#                base.depts[line], horizontalalignment='left',
#                size='x-small', color='black', weight='semibold')

plt.show()


base2 = data_depts[data_depts.quantidade_artigos > 50]
base2['depts'] = base.index
base2.columns = ['novelty', 'transience', 'ressonance', 'citations',
                 'num-authors', 'amount_papers', 'mean_ressonances',
                 'member', 'depts']

plot2 = sns.scatterplot(data=base2, x='novelty', y='ressonance',
                        size='amount_papers')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.axvline(mean_depts_novelty, color='gray')
plt.axhline(mean_depts_ressonance, color='gray')


for line in range(base2.shape[0]):
    if base2.depts[line] == 'caen':
        plot2.text(base2.novelty[line]+0.03, base2.ressonance[line]-0.01,
                   base2.depts[line], horizontalalignment='left',
                   size='x-small', color='black', weight='semibold')

    elif base2.depts[line] == 'unicamp':
        plot2.text(base2.novelty[line]+0.03, base2.ressonance[line]-0.01,
                   base2.depts[line], horizontalalignment='left',
                   size='x-small', color='black', weight='semibold')

    elif base2.depts[line] == 'ufu':
        plot2.text(base2.novelty[line]-0.05, base2.ressonance[line]+0.02,
                   base2.depts[line], horizontalalignment='left',
                   size='x-small', color='black', weight='semibold')

    elif base2.depts[line] == 'ufjf':
        plot2.text(base2.novelty[line]-0.12, base2.ressonance[line],
                   base2.depts[line], horizontalalignment='left',
                   size='x-small', color='black', weight='semibold')

    else:
        plot2.text(base2.novelty[line]+0.018, base2.ressonance[line],
                   base2.depts[line], horizontalalignment='left',
                   size='x-small', color='black', weight='semibold')

plt.show()
