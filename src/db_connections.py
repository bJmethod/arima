import pandas as pd
from sqlalchemy import create_engine
import psycopg2
import logging

def get_to_from(conn, id_numerico):

    get_to_from_historic_query = f""" 
         select confarimacabezalhistoricodesde as aniodesde, confarimacabezalhistoricohasta as aniohasta
         from confarimacabezal
         where confarimacabezalid= {id_numerico} 
             """
    df = pd.read_sql(get_to_from_historic_query, conn)
    return df
def get_forecast_year(conn,id_numerico):
    get_to_from_forecast_query = f""" 
        select CONFARIMACABEZALPROYECCIONDESD as aniodesde, CONFARIMACABEZALPROYECCIONHAST as aniohasta
        from confarimacabezal
        where confarimacabezalid= {id_numerico} 
            """

    df = pd.read_sql(get_to_from_forecast_query, conn)
    return df
def get_data_forecast(conn,anio_desde, anio_hasta,indice ):
    get_data_query = f"""
            select anionro as anio, HISTORICOMES as mes, HISTORICOCREDVIG  as valor
            from HISTORICO
            where anionro >= {anio_desde} and anionro<= {anio_hasta} and HISTORICOINDICE = {indice} order by anio,mes
            """
    df = pd.read_sql(get_data_query, conn)
    return df
def update_model_spec_query(valor_ar, valor_i,valor_ma,id_numerico, indice):
    query = f'''
    update confarimaresultado set confarimaar={valor_ar},
    confarimai= {valor_i}, confarimama= {valor_ma}
    where  confarimacabezalid= {id_numerico} and
    confarimaindice= {indice}
    '''
    return query


def update_valor_forecast( valor, id_numerico, indice, anio, mes):
    ## this function can update the bd of forecast
    # so if i have
    # {"month": [1, 2], "valor": forecast} update -> bd

    query = f''' 
        update confarimamodeloaplicado
        set procesado=TRUE,
        confarimamodeloaplicadoporc={valor}
        where confarimacabezalid={id_numerico} and
        confarimamodeloaplicadoindice= {indice}
        and confarimamodeloaplicadoanio = {anio} and confarimamodeloaplicadomes = {mes}

    '''
    ######################################################################################
    ##### GABRIEL: falta agregar esto a el query de arriba
    ##### and confarimamodeloaplicadoanio = 2031 and confarimamodeloaplicadomes = 3
    ##### GABRIEL: aca puse 2031 y 3, pero deberian de ser el mes y año del resultado
    print(f"update_valor_forecast={query}")
    return query
def get_conn(host, db, user, password,port):
    print("conecting to db..")
    conexion = psycopg2.connect(host=host, database=db, user=user, password=password,port=port)

    return conexion
def get_engine(conn):
    engine = create_engine('postgresql+psycopg2://', creator=lambda: conn)
    return engine
def get_data(conn, id_numerico,indice):
    logging.info(f'getting data for {id_numerico}')
    forecast_year = get_to_from(conn, id_numerico) # GABRIEL de aca se saca desde y hasta a tomar del historico
    # forecast_year -> {"aniodesde":[1],"aniohasta":[2]}
    anio_desde= forecast_year.aniodesde[0]
    anio_hasta = forecast_year.aniohasta[0]
    print(f"anio_desde historico = {anio_desde}")
    print(f"anio_hasta historico = {anio_hasta}")
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
    print(f"updated {type} {id_numerico}")
    print(f" update query {query}")

def load_forecast_info(conn,id_numerico: int ,valor_ar: int, valor_i:int,valor_ma: int, indice:str):
    #completar estos dos metodos
    update_espec_query = update_model_spec_query(valor_ar, valor_i,valor_ma,id_numerico, indice)
    __do_update(conn,update_espec_query,id_numerico,'specs')
    print(f"finish load model info for {id_numerico}")


def load_forecast_values(conn, id_numerico:int, indice:str, valores: list, anio,mes: object) :
    for l in mes:
        m = l+1
        ##redondeamos millones
        valor = round(valores[l]/1000000,13)
        print(valor, id_numerico,  indice, m )
        anio = int(anio)
        update_valor_forecast(valor, id_numerico, indice, anio, mes)
        query_update_forcast = update_valor_forecast(valor, id_numerico, indice,anio, mes = m)

        __do_update(conn,query_update_forcast, id_numerico ,'update_forecast')
           # get_data(host, db, user, password, id_numerico)->{"data": df -> data to  learn,
           #  "ind_proyeccion": pr_time -> time to forecast}
