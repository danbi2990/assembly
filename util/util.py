# import pandas as pd


def save_df_to_tsv(df, destination, index=False):
    tsv = df.to_csv(sep='\t', index=index)
    with open(destination, 'w') as f:
        f.write(tsv)
