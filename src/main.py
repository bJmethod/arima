import sys
from model import model
from sensitive import sensitive_dict
from db_connections import get_data, get_conn,load_forecast_info,load_forecast_values, get_engine, insert_log
from utils import interpret_steps, integrate_series
import logging

## Refactor generar varios logs por  IDarima_indice.log ej : 7_2872.log
user = sensitive_dict()['usr']
password = sensitive_dict()['password']
host = sensitive_dict()['host']
port = sensitive_dict()['puerto']
db = sensitive_dict()['db']
LOG_RUTE = sensitive_dict()['log_dir']
id_numerico= sys.argv[1]
indice = sys.argv[2]



logging.basicConfig(filename=f'{LOG_RUTE}/{id_numerico}_{indice}.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

conn = get_conn(host, db, user, password,port)

engine =get_engine(conn)

d = get_data(conn,engine, id_numerico,indice)

df = d['data']

time_to_forecast = d["ind_proyeccion"]
Xt = df["valor"]

insert_log(conn, id_numerico, indice,'main.py', 'CABEZAL ARIMA = '+str(id_numerico)+ ' INDICE='+str(indice))
json_str = df.to_json(orient='records', lines=True)
insert_log(conn, id_numerico, indice,'main.py', 'HISTORICO = '+json_str)
json_str = Xt.to_json(orient='records', lines=True)
insert_log(conn, id_numerico, indice,'main.py', 'XT = '+json_str)
logging.info(f"historico {json_str}")


## estimate model
model = model(Xt, True, [], True)
model.get_arima()

## esto está arrojando un vector de forecast tamaño 2 y deberia ser tamaño 18
anio_hasta = time_to_forecast.aniohasta.values[0]
anio_desde = time_to_forecast.aniodesde.values[0]
insert_log(conn, id_numerico, indice,'main.py', 'PROYECCION desde='+str(anio_desde)+ ' hasta='+str(anio_hasta))
logging.info(f"proyeccion desde {anio_desde} hasta {anio_hasta}")


steps_interpreted = interpret_steps(anio_desde, anio_hasta)
steps = steps_interpreted["steps"]
logging.info(f"LOG= forcasting for {steps} preiods ahead from {anio_desde} to {anio_hasta} ")
insert_log(conn, id_numerico, indice,'main.py', 'Proy de '+str(steps)+ ' periodos en '+str(anio_desde)+ ' a '+str(anio_hasta))

model.forecast(int(steps))

valoresD = model.predictions if model.predictions is not None else insert_log(conn, id_numerico, indice,'main.py', 'No podemos predecir: id '+str(id_numerico)+ ' indice '+str(indice))
valores = integrate_series(valoresD, Xt)

insert_log(conn, id_numerico, indice,'main.py', 'Queremos insertar: '+str(valores))
logging.info('Queremos insertar: '+str(valores))
valor_ar, valor_i, valor_ma = model.manual.order
## update values

id = int(id_numerico)
load_forecast_info(conn,id,valor_ar, valor_i,valor_ma, indice)

insert_log(conn, id_numerico, indice,'main.py', 'update for id '+str(id)+ ' valores '+str(valores))
if valores is not None:
    load_forecast_values(conn, id, indice, valores,anio_desde)

