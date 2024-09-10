import pandas as pd
from src.model import model
from src.utils import integrate_series
from src.db_connections import *

# Definir la función de procesamiento para cada hoja
def process_sheet(sheet_name, df):
    # Renombrar columnas
    df.rename(columns={"historicoporccomp": "valor"}, inplace=True)

    # Limpiar los años de acuerdo a la lógica de la función (esta función debes definirla o adaptarla)
    #cleaning_years = excluir_anio_credito(df, 1, 2, 'conn')

    Xt = df["valor"]

    # Ajustar el modelo
    modelo = model(Xt, True, [], True)
    modelo.get_arima()
    modelo.forecast(18)
    valoresD = modelo.predictions

    # Integrar las series para obtener la serie pronosticada
    if len(valoresD)>0 :
        valores = integrate_series(valoresD, Xt)

        # Crear un DataFrame con los resultados
        df_result = pd.DataFrame(valores, columns=["pronostico"])
        df_result.to_csv("pronostico_bug.csv",index= False)
        # Retornar los resultados
        return df_result


if __name__ == '__main__':
    # Leer todas las hojas del archivo Excel
    file_path = 'C:/Users/Usuario/OneDrive/Documentos/projects/arima/src/resources/10589.xlsx'
    sheets = pd.read_excel(file_path, sheet_name=None)

    # Diccionario para almacenar los resultados de cada hoja
    results = {}

    # Procesar cada hoja y guardar los resultados en el diccionario
    for sheet_name, df in sheets.items():
        df_result = process_sheet(sheet_name, df)
        results[f"f pronostico {sheet_name}"] = df_result

