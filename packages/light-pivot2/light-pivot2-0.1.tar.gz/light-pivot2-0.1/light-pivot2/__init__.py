import pandas as pd
import numpy as np

def start():
    print("import successful")

def add(a, b):
    return a + b

def FE_pivot(train, test, keys, col, val=None, op='sum'):
    print(keys, col, val, op)
    cols_sel = keys + [col] if col not in keys else keys
    cols_sel = cols_sel + [val] if val is not None else cols_sel
    df = pd.concat([train[cols_sel], test[cols_sel]], axis=0).reset_index(drop=True)

    df['values'] = 1
    df = pd.pivot_table(df,
                        index=keys,
                        values=['values'] if val is None else [val],
                        # values=['values'],
                        columns=[col],
                        aggfunc=op,
                        fill_value=0)
    df.columns = [str(col) + '_' + str(c[0]) + '_' + str(c[1]) + '_' + str(op) for c in df]
    df.reset_index(inplace=True)
    return df

def get_label():
    return [1,2,3]

