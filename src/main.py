from src.model import model
import pandas as pd

if __name__ == "__main__":
     df = pd.read_excel("C:/Users/Usuario/Documents/Arima.xlsx", skiprows=1)
     Xt = df[['Ejecución Comprometida']].copy()
     Xt.rename(columns={'Ejecución Comprometida': 'ejec_cp'}, inplace=True)
     model = model(Xt, True, [], True)
     a = 1
     model.get_arima()
     model.forecast(2)
     a += 1


