import pandas as pd
from sqlalchemy import create_engine
import psycopg2
import logging
from src.utils import *

def get_to_from(conn, id_numerico) -> object:

    get_to_from_historic_query = f""" 
         select confarimacabezalhistoricodesde as aniodesde, confarimacabezalhistoricohasta as aniohasta
         from confarimacabezal
         where confarimacabezalid= {id_numerico} 
             """
    df = pd.read_sql(get_to_from_historic_query, conn)
    return df
def get_forecast_year(conn,id_numerico) -> object:
    get_to_from_forecast_query = f""" 
        select CONFARIMACABEZALPROYECCIONDESD as aniodesde, CONFARIMACABEZALPROYECCIONHAST as aniohasta
        from confarimacabezal
        where confarimacabezalid= {id_numerico} 
            """

    df = pd.read_sql(get_to_from_forecast_query, conn)
    return df
def get_data_forecast(conn,anio_desde, anio_hasta,indice ) :
    get_data_query = f"""
            select anionro as anio, HISTORICOMES as mes, historicoporccomp  as valor
            from HISTORICO
            where anionro >= {anio_desde} and anionro<= {anio_hasta} and HISTORICOINDICE = {indice} order by anio,mes
            """
    df = pd.read_sql(get_data_query, conn)
    return df


def update_model_spec_query(valor_ar, valor_i,valor_ma,id_numerico, indice) -> str:
    query = f'''
    update confarimaresultado set confarimaar={valor_ar},
    confarimai= {valor_i}, confarimama= {valor_ma}
    where  confarimacabezalid= {id_numerico} and
    confarimaindice= {indice}
    '''
    return query


def update_valor_forecast( valor, id_numerico, indice, anio, mes) -> str:

    query = f''' 
        update confarimamodeloaplicado
        set procesado=TRUE,
        confarimamodeloaplicadoporc={valor}
        where confarimacabezalid={id_numerico} and
        confarimamodeloaplicadoindice= {indice}
        and confarimamodeloaplicadoanio = {anio} and confarimamodeloaplicadomes = {mes}

    '''

    print(f"update_valor_forecast={query}")
    return query


def get_conn(host, db, user, password,port):

    print("conecting to db..")
    try:

        conexion = psycopg2.connect(host=host, database=db, user=user, password=password,port=port)
    except Exception as e:

        logging.ERROR(f"cant coneect exception {e}")

        conexion = None
    return conexion


def get_engine(conn):

    try:

        engine = create_engine('postgresql+psycopg2://', creator=lambda: conn)
    except Exception as e:
        logging.ERROR(f"can´t create engine {e}")
        engine = None
    return engine


def get_data(conn, id_numerico,indice):
    logging.info(f'getting data for {id_numerico}')
    forecast_year = get_to_from(conn, id_numerico) # GABRIEL de aca se saca desde y hasta a tomar del historico
    # forecast_year -> {"aniodesde":[1],"aniohasta":[2]}
    anio_desde= forecast_year.aniodesde[0]
    anio_hasta = forecast_year.aniohasta[0]
    logging.info(f"anio_desde historico = {anio_desde}")
    logging.info(f"anio_hasta historico = {anio_hasta}")
    df = get_data_forecast(conn, anio_desde, anio_hasta, indice) ## GABRIEL se pasa indice para obtener los datos del historico
    logging.info(f'finishing geting data {anio_desde} {anio_hasta} and indice {indice}')
    pr_time = get_forecast_year(conn,id_numerico) #GABROEÑ esta bien pasar el id, que es la clave en el cabezal arima
    logging.info(f' years for fore cast {pr_time}')
    return {"data": df,
            "ind_proyeccion": pr_time}


def __do_update(conn,query,id_numerico,type):
    cur = conn.cursor()
    logging.info(f'updating with {query} for {id_numerico}')
    cur.execute(query)
    conn.commit()
    logging.info(f"updated {type} {id_numerico}")
    logging.info(f" update query {query}")


def load_forecast_info(conn,id_numerico: int ,valor_ar: int, valor_i:int,valor_ma: int, indice:str):
    update_espec_query = update_model_spec_query(valor_ar, valor_i,valor_ma,id_numerico, indice)
    __do_update(conn,update_espec_query,id_numerico,'specs')
    logging.info( f"finish load model info for {id_numerico}")




def load_forecast_values(conn, id_numerico:int, indice:str, valores: list, anio,) :
    for i, l in enumerate(valores):
        m = interpret_months(i)
        valor = round(valores[i],3)
        print(f" inserting value {valor}, in {id_numerico},  for {indice}, month {m} " )
        anio_actual = interpret_year(anio,i)
        query_update_forcast = update_valor_forecast(valor, id_numerico, indice,anio_actual, mes = m)
        __do_update(conn,query_update_forcast, id_numerico ,'update_forecast')



