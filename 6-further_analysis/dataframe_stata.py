"""Script to make an excel file to stata software (reg)."""

import os
import pandas as pd


root = os.path.abspath(os.curdir)
local_final = r'dados/data_final'

# =============================================================================
# First treatment of databases
# =============================================================================

kld = pd.read_pickle(f'{root}/{local_final}/data_KLDv4(30_gensim).pkl')
data = pd.read_pickle(f'{root}/{local_final}/data_final_v2.pkl')
matches = pd.read_pickle(f'{root}/dados/outside/matches.pkl')

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
cols = cols[0:6] + cols[-21:] + cols[6:-21]
citations_base = citations_base[cols]

citations_base['code_area'] = data.code_area

cols = citations_base.columns.to_list()
cols = cols[0:4] + cols[-1:] + cols[4:30]
df = citations_base[cols]

del cols

df = df[~df.index.duplicated(keep='first')]

df_merge = pd.merge(kld, df,
                    left_index=True,
                    right_index=True).drop_duplicates()

df_merge = pd.merge(df_merge, matches, left_index=True, right_index=True)

corr = df_merge.corr()

df_merge.to_excel(f'{root}/dados/outside/base_stata.xlsx')

corr = df_merge.corr()
