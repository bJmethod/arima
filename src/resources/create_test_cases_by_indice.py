import pandas as pd
from random import sample
def read_main_file_and_split_by_indice(file):
 df = pd.read_excel(f"{file}.xlsx")
 ### elije 20 indices al azar y crea el caso de prueba
 indices = sample(list(df['historicoindice'].unique()),20)
 for indice in indices:
     # Filtra los datos para el índice actual
     df_temporal = df[df['historicoindice'] == indice].copy()
     nombre_dataframe = f"{file}_{indice}.csv"
     df_temporal.to_csv(nombre_dataframe, index= False)

if __name__== '__main__':
    read_main_file_and_split_by_indice("historico")