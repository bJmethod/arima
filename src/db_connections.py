import psycopg2
import pandas as pd



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
        select confarimacabezalproyecciondesde as aniodesde, confarimacabezalproyeccionricohasta as aniohasta
        from confarimacabezal
        where confarimacabezalid= {id_numerico} 
            """

    df = pd.read_sql(get_to_from_forecast_query, conn)
    return df
def get_data_forecast(conn,anio_desde, anio_hasta,id_numerico ):
    get_data_query = f""""
            select anionro as anio, datoshistoricoejincmes as mes, datoshistoricoejinccredvi as valor
            from datoshistoricoejinc
            where anionro >= {anio_desde} and anionro<= {anio_hasta} and datoshistoricoejincindice = {id_numerico}
            """
    df = pd.read_sql(get_data_query, conn)
    return df
def update_model_spec_query(valor_ar, valor_i,valor_ma,id_numerico, indice):
    query = f'''
    update confarimaresultado set confarimaar={valor_ar},
    confarimai= {valor_i}, confarimama= {valor_ma},
    where  confarimacabezalid= {id_numerico} and
    confarimaindice= {indice}
    '''
    return query
def update_valor_forecast(valor,id_numerico,indice):
    ## this function can update the bd of forecast
    # so if i have
    # {"month": [1, 2], "valor": forecast} update -> bd

    query = f''' 
        update confarimamodeloaplicado
        set confarimamodeloaplicadoprocesa=TRUE,
        confarimamodeloaplicadoporc={valor}
        and confarimacabezalid={id_numerico} and
        confarimamodeloaplicadoindice= {indice};
    '''
    return query
def get_conn(host, db, user, password):
    print("conecting to db..")
    conexion = psycopg2.connect(host=host, database=db, user=user, password=password)
    return conexion

def get_data(host, db, user, password, id_numerico):
    conn = get_conn(host, db, user, password)
    forecast_year = get_forecast_year(conn, id_numerico)
    # forecast_year -> {"aniodesde":[1],"aniohasta":[2]}
    anio_desde= forecast_year.aniodesde[0]
    anio_hasta = forecast_year.aniohasta[0]
    df = get_data_forecast(conn, anio_desde, anio_hasta, id_numerico)
    pr_time = get_forecast_year(conn,id_numerico)
    return {"data": df,
            "ind_proyeccion": pr_time}
def __do_update(conn,query,id_numerico,type):
    cur = conn.cursor()
    cur.execute(query)
    print(f"updated {type} {id_numerico}")

def load_forecast_info(conn,id_numerico,valor_ar, valor_i,valor_ma, indice):
    #completar estos dos metodos
    update_espec_query = update_model_spec_query(valor_ar, valor_i,valor_ma,id_numerico, indice)
    __do_update(conn,update_espec_query,id_numerico,'specs')
    print(f"finish load model info for {id_numerico}")


def load_forecast_values(conn, id_numerico:int, indice:str, valores: list) :
    for valor in valores:
        query_update_forcast = update_valor_forecast(valor, id_numerico, indice)
        __do_update(conn,query_update_forcast, id_numerico,'update_forecast')
           # get_data(host, db, user, password, id_numerico)->{"data": df -> data to  learn,
           #  "ind_proyeccion": pr_time -> time to forecast}
