import sys
from model import model
from sensitive import sensitive_dict

from db_connections import get_data, get_conn,load_forecast_info,load_forecast_values, get_engine


user = sensitive_dict()['usr']
password = sensitive_dict()['password']
host = sensitive_dict()['host']
port = sensitive_dict()['puerto']
db = sensitive_dict()['db']

id_numerico= sys.argv[1]
indice = sys.argv[2]
conn = get_conn(host, db, user, password,port)
engine =get_engine(conn)
d = get_data(engine, id_numerico,indice)  # GABRIEL, se debe de pasar ambos, el id, para obtener desde y hasta para obtener datos del historico, y
                                        # año desde y hasta de la proyeccion, eso desde el cabezal arima, y luego indic

df = d['data']
ind_forecast = d["ind_proyeccion"]
Xt = df["valor"]
print(f"CABEZAL ARIMA = {id_numerico}")
print(f"INDICE =  {indice}")
print(f"DATA ={df}")
print(f"IND_FOR = {ind_forecast}")
print(f"XT =  {Xt}")

## estimate model
model = model(Xt, True, [], True)
model.get_arima()
steps = len(ind_forecast)
model.forecast(steps)
valores = model.predictions
valor_ar, valor_i, valor_ma = model.model.order
## update values

id = int(id_numerico)
load_forecast_info(conn,id,valor_ar, valor_i,valor_ma, indice)
load_forecast_values(conn, id, indice, valores)


##test case
# if __name__ == "__main__":
#      df = pd.read_excel("C:/Users/Usuario/Documents/Arima.xlsx", skiprows=1)
#      Xt = df[['Ejecución Comprometida']].copy()
#      Xt.rename(columns={'Ejecución Comprometida': 'ejec_cp'}, inplace=True)
#      model = model(Xt, True, [], True)
#      a = 1
#      model.get_arima()
#      model.forecast(2)
#      f= model.model.order
#      forecast = model.predictions
#      new_Data =  pd.DataFrame({"month":[1,2],"valor": forecast})
#      a += 1
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


