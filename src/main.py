from model import model
from sensitive import sensitive_dict
from db_connections import get_data
import pandas as pd

if __name__ == "__main__":
     df = pd.read_excel("C:/Users/Usuario/Documents/Arima.xlsx", skiprows=1)
     Xt = df[['Ejecución Comprometida']].copy()
     Xt.rename(columns={'Ejecución Comprometida': 'ejec_cp'}, inplace=True)
     model = model(Xt, True, [], True)
     a = 1
     model.get_arima()
     model.forecast(2)
     forecast = model.predictions
     new_Data =  pd.DataFrame({"month":[1,2],"valor": forecast})
     a += 1
     # sensitive_data = sensitive_dict()
     # user = sensitive_data["usr"]
     # password= sensitive_data["password"]
     # host = sensitive_data["password"]
     # db = 'db'
     # data = get_data(host, db, user, password, id_numerico)
          #->{"data": df -> data to  learn,
           #  "ind_proyeccion": pr_time -> time to forecast}

## log de un disclaimer
## log al inicio al final


