import sys
from model import model
from sensitive import sensitive_dict

from db_connections import get_data, get_conn,load_forecast_info,load_forecast_values, get_engine
import logging

user = sensitive_dict()['usr']
password = sensitive_dict()['password']
host = sensitive_dict()['host']
port = sensitive_dict()['puerto']
db = sensitive_dict()['db']


def interpret_steps(aniodesde, aniohasta):
    steps_ahead = int((aniohasta - aniodesde + 1)*18)
    diff = aniohasta - aniodesde + 1
    years_forecast = [aniodesde + i for i in range(0, diff)]
    return {"steps": steps_ahead, "anio_desde": aniodesde}

id_numerico= sys.argv[1]
indice = sys.argv[2]

logging.basicConfig(filename=f'{id_numerico}_arima.log.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

conn = get_conn(host, db, user, password,port)
engine =get_engine(conn)
d = get_data(engine, id_numerico,indice)  # GABRIEL, se debe de pasar ambos, el id, para obtener desde y hasta para obtener datos del historico, y
                                        # año desde y hasta de la proyeccion, eso desde el cabezal arima, y luego indic

df = d['data']
print(f"HISTORICO = {df}")
time_to_forecast = d["ind_proyeccion"]
Xt = df["valor"]
print(f"CABEZAL ARIMA = {id_numerico}")
print(f"INDICE =  {indice}")
#print(f"DATA ={df}")
print(f"IND_FOR = {time_to_forecast}")
print(f"XT =  {Xt}")

## estimate model
model = model(Xt, True, [], True)
model.get_arima()


## esto está arrojando un vector de forecast tamaño 2 y deberia ser tamaño 18
anio_hasta = time_to_forecast.aniohasta.values[0]
anio_desde = time_to_forecast.aniodesde.values[0]
steps_interpreted = interpret_steps(anio_desde, anio_hasta)
steps = steps_interpreted["steps"]
print(f"LOG= forcasting for {steps} preiods ahead from {anio_desde} to {anio_hasta} ")
model.forecast(int(steps))
valores = model.predictions

valor_ar, valor_i, valor_ma = model.model.order
## update values

id = int(id_numerico)
load_forecast_info(conn,id,valor_ar, valor_i,valor_ma, indice)
print(f"update for id {id} valores {valores}")

## falta resolver esto porque hay que iterar sobre anio o pasarle una lista y resolverlo db(not so fan)
load_forecast_values(conn, id, indice, valores.values,anio_desde)


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


