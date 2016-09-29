from __future__ import print_function, division
import pandas as pd


def split(df):
    title_column = df.columns[0]
    titles = df[title_column]

    for value_column in df.columns[1:]:
        df_split = pd.concat([titles, df[value_column]], axis=1)
        yield df_split

SEP = ';'

df = pd.read_csv('all_years.csv', sep=SEP)
dfs_split = split(df)
for df_split in dfs_split:
    fname = '{}.yaml'.format(df_split.columns[1])
    s = df_split.to_csv(header=False, sep=SEP, index=False)
    s_new = s.replace(SEP, ': ')
    with open(fname, 'w') as f:
        f.write(s_new)
