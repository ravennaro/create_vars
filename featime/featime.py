# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_featime.ipynb.

# %% auto 0
__all__ = ['mode', 'featime_in_time']

# %% ../nbs/00_featime.ipynb 3
from fastcore.test import *
from fastcore.utils import *
import pandas as pd

# %% ../nbs/00_featime.ipynb 5
def mode(x):
    return pd.Series.mode(x).values[0]

# %% ../nbs/00_featime.ipynb 12
def featime_in_time(df_, # Dataframe
                        id_cols, # Colunas de agrupamento como id e safra
                        trns_time_var:str, # Data correspondente a variável 
                        ref_time_var:str, # Data que será a referência para calcular as janelas de tempo 
                        value_vars:list, # Lista das variáveis que serão calculadas as operações
                        window:list, # Lista contendo a janela para calcular as variáveis 
                        operations:list # Lista das operações a serem calculadas
                        ): 
    
    df = df_.copy()
    df[trns_time_var] = pd.to_datetime(df[trns_time_var], format='%Y%m%d')
    df[ref_time_var] = pd.to_datetime(df[ref_time_var], format='%Y%m%d')
    df_spine =  df[id_cols].drop_duplicates()

    for var in value_vars:
        for size in window:
           
            time_cond = (df[trns_time_var] < df[ref_time_var]) & (df[trns_time_var] >= df[ref_time_var] + pd.DateOffset(months=size))
            df_grouped = df[time_cond].groupby(id_cols).agg({var:operations})
            df_grouped.columns = ['_'.join(col).strip()+'_'+str(abs(size))+'M' for col in df_grouped.columns.values]
            df_grouped.reset_index(inplace=True)
            df_spine = df_spine.merge(df_grouped,on=id_cols,how='left')

           
    return df_spine