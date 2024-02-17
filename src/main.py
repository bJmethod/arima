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
id_numerico= sys.argv[1]
indice = sys.argv[2]

def interpret_steps(aniodesde, aniohasta):
    steps_ahead = int((aniohasta - aniodesde + 1)*18)
    return {"steps": steps_ahead, "anio_desde": aniodesde}


logging.basicConfig(filename=f'{id_numerico}_arima.log.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

conn = get_conn(host, db, user, password,port)

engine =get_engine(conn)

d = get_data(engine, id_numerico,indice)

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

load_forecast_values(conn, id, indice, valores.values,anio_desde)
