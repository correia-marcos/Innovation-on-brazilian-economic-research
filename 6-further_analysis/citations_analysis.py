"""
This script was made to anaylse the matches between comission and coautors.

(In terms of departaments!)

VERY IMPORTANT: The citation database was partly created out of this python
project.
We googled the paper and save the quantity of citation in a excel file that
is now located on "dados" file.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import scipy.stats as st

root = os.path.abspath(os.curdir)
local_final = r'dados/data_final'

# =============================================================================
# First treatment of databases
# =============================================================================

data = pd.read_pickle(f'{root}/{local_final}/data_final_v2.pkl')

data['docs'] = data.index
data['ano'] = data.docs.str.split('_')
data.loc[:, 'ano'] = data.ano.map(lambda x: x[1])
data = data.drop('docs', 1)

# this was done because there was a line that did not have any papers
# (was a mistake in the scraping process)

data = data[data.linguagem.notna()]
# data.to_pickle(f'{root}/{local_final}/data_final_v2.pkl')

xls = pd.ExcelFile(f'{root}/dados/outside/citations.xlsx')
citations_base = pd.read_excel(xls, 'base', index_col='doc_num')
reviewers_base = pd.read_excel(xls, 'revieweres')
size_base = pd.read_excel(xls, 'size')
size_base = size_base[size_base.is_member == 1]
size_base = size_base[size_base.ANPEC != '-']


citations_base['docs'] = citations_base.index
citations_base['ano'] = citations_base.docs.str.split('_')
citations_base.loc[:, 'ano'] = citations_base.ano.map(lambda x: x[1])
citations_base = citations_base.drop('docs', 1)

cols = citations_base.columns.to_list()
cols = cols[0:5] + cols[-1:] + cols[5:-1]
citations_base = citations_base[cols]


df = pd.merge(citations_base, data.code_area, left_index=True,
              right_index=True)
df = df.drop('citations1', 1)

cols = df.columns.to_list()
cols = cols[1:4] + cols[-1:] + cols[4:10]
df = df[cols]

df['papers'] = df.index

del cols
# =============================================================================
# Simulations
# =============================================================================

lista_col = ['title', 'Area', 'code_area', 'lang', 'ano', 'citations', 'Type',
             'num-authors', 'papers']


def get_deprt(lista):
    """Add together from row with same index."""
    base = []
    for item in lista:
        base.append(item)

    resultado = set(base)
    return resultado


data_df = df.groupby(lista_col)['Dept'].apply(lambda x:
                                              get_deprt(x)).reset_index()
data_df = data_df.set_index(data_df.papers).sort_index()
data_df = data_df.drop('papers', 1)
data_df.ano = pd.to_numeric(data_df.ano)

del lista_col


def get_df_matches(df1, df2):
    """
    Calculate the amount of matches between comission departments and autors.

    Parameters
    ----------
    df1 : DataFrame
        DataFrame containing a column named 'Dept' with a list/set of depts
        in each paper (papers are the index).
    df2 : DataFrame
        DataFrame containing the comission departaments in the column 'depts'.

    Returns
    -------
    DataFrame containg two columns: one with a tuple of the departments (for
    validation) and one with the amount of matches for the paper index.

    Sum of all matches in the above dataframe.
    """
    groups = df1.groupby(['code_area', 'ano'])
    dfs = dict(tuple(groups))

    groups_review = df2.groupby(['code_area', 'ano'])
    dfs_review = dict(tuple(groups_review))

    dicionario_lengh = {}
    dictionario_depts = {}
    for keys in dfs_review:
        depart = set(dfs_review[keys].depts)
        for index, row in dfs[keys].iterrows():
            dictionario_depts[index] = tuple(depart.intersection(row.Dept))
            dicionario_lengh[index] = len(depart.intersection(row.Dept))

    data_len = pd.DataFrame.from_dict(dicionario_lengh, orient='index',
                                      columns=['matches'])
    data_deps = pd.DataFrame.from_dict(dictionario_depts, orient='index',)
    data_deps['depts'] = data_deps.values.tolist()
    data_deps = data_deps.drop(data_deps.columns.difference(['depts']), 1)

    data_final = pd.merge(data_deps, data_len, left_index=True,
                          right_index=True)
    sum_data_final = data_final.matches.sum()

    return sum_data_final, data_final


def get_df_matches_simulation(df1, df2, df3_size):
    """
    Calculate the amount of matches between comission departments and autors.

    Similar behavior of the other function, but tries to simulate with
    random sampled comissions (simulations).
    Other difference is that this function only saves the sum of all matches
    in each simulation.
    Parameters
    ----------
    df1 : DataFrame
        DataFrame containing a column named 'Dept' with a list/set of depts
        in each paper (papers are the index).
    df2 : DataFrame
        DataFrame containing the comission departaments in the column 'depts'.
    df3: Dataframe
        DataFrame containing the size of each department (data from
                                                          dados/outside)
    n: int
        number of repetion of the process.
    Returns
    -------
    DataFrame containg three columns: areas, year and amount of matches
    for each paper (index).

    Sum of all matches in the above dataframe.
    """
    list_departs = df3_size.ANPEC.to_list()
    list_weights = df3_size.CAPES_size.to_list()

    array_weights = np.asarray(list_weights)
    array_weights = array_weights/(array_weights.sum())

    groups = df1.groupby(['code_area', 'ano'])
    dfs = dict(tuple(groups))

    groups_review = df2.groupby(['code_area', 'ano'])
    dfs_review = dict(tuple(groups_review))

    dicionario_lengh = {}

    for keys in dfs_review:
        area, ano = keys
        rows = dfs_review[keys].shape[0]
        random_depts = np.random.choice(list_departs,
                                        p=array_weights,
                                        size=rows,
                                        replace=False)
        depts_set = set(map(str, random_depts))
        for index, row in dfs[keys].iterrows():
            dicionario_lengh[index] = len(
                depts_set.intersection(row.Dept))
    data_len = pd.DataFrame.from_dict(dicionario_lengh, orient='index',
                                      columns=['matches'])

    sum_data_len = data_len.matches.sum()

    return sum_data_len, data_len


def get_df_matches_simulation_ntimes(df1, df2, df3_size, n):
    """Do the 'get_df_matches_simulation' n-times and take median result."""
    list_dfs_matches = []
    list_sum_dfs_matches = []
    for i in range(n):
        soma, df_match = get_df_matches_simulation(data_df, reviewers_base,
                                                   size_base)
        list_dfs_matches.append(df_match)
        list_sum_dfs_matches.append(soma)
    array_sum = np.asarray(list_sum_dfs_matches)
    df_concat = pd.concat((i for i in list_dfs_matches), axis=1)

    return array_sum, df_concat


num_base, base = get_df_matches(data_df, reviewers_base)
num_simu, base_simu = get_df_matches_simulation_ntimes(data_df,
                                                       reviewers_base,
                                                       size_base,
                                                       1000)


# =============================================================================
# Final results
# =============================================================================

media_simu = np.average(num_simu)
std_simu = np.std(num_simu)

intervalo = st.t.interval(0.95, len(num_simu)-1,
                          loc=np.mean(num_simu), scale=st.sem(num_simu))

final_base = pd.DataFrame({'média': media_simu,
                           'desvio padrão': std_simu,
                           'intervalo de confiança (95%)': intervalo})

# final_base.to_excel(f'{root}/dados/outside/resultados_matches.xlsx')
final_base.to_excel(f'{root}/dados/outside/resultados_matchesv2.xlsx')

# =============================================================================
# Plots
# =============================================================================
# sns.set_style('whitegrid')
# sns.set(style='white')
# sns.color_palette("flare", as_cmap=True)
# sns.set_context('paper')

lista = [f'random_{i}' for i in range(1, 1001)]
lista.append('true_matches')

num_simu_plot = np.append(num_simu, num_base)

data_plot = pd.DataFrame(data=num_simu_plot,
                         index=lista)

listinha = ['random_matches' for n in range(1, 1001)]
listinha.append('true_matches')

data_plot.columns = ['matches']
data_plot['random'] = listinha

plt.rcParams["patch.force_edgecolor"] = True

sns.histplot(data_plot, x='matches',
             stat='density',
             cbar_kws=dict(edgecolor="black", linewidth=10))
plt.plot([data_plot[data_plot['random'] == 'true_matches'].matches.iloc[0],
          data_plot[data_plot['random'] == 'true_matches'].matches.iloc[0]],
         [0, 0.02], color='black')
plt.show()

# =============================================================================
# Plot for area
# =============================================================================
base[['code_area', 'ano']] = data_df[['code_area', 'ano']]
base_simu[['code_area', 'ano']] = data_df[['code_area', 'ano']]

base['matches_total'] = num_base
# base.to_pickle(f'{root}/dados/outside/simulation/base_real.pkl')
# base_simu.to_pickle(f'{root}/dados/outside/simulation/base_simu.pkl')

gb_base = base.groupby(['code_area'])
dfs_base = dict(tuple(gb_base))

gb_base_simu = base_simu.groupby(['code_area'])
dfs_base_simu = dict(tuple(gb_base_simu))


list_test = []
for keys in dfs_base:
    teste = dfs_base_simu[keys]['matches']
    teste['true_matches'] = dfs_base[keys].matches
    list_test.append(teste)

j = 1
for i in list_test:
    # i['area'] = data_df['Area']
    teste2 = pd.DataFrame(i.sum(), columns=['matches'])
    sns.histplot(teste2, x='matches', stat='density')
    plt.title(f'Area {j}')
    plt.plot([teste2.loc['true_matches', 'matches'],
              teste2.loc['true_matches', 'matches']],
             [0, 0.05], color='black')
    plt.show()
    j += 1
