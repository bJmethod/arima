import psycopg2
import pandas as pd
HOST= "host"
DB= "db"
USER = "user"
PASSWORD= "pss"
id_numerico = 21



anio_desde = 21
anio_hasta= 21


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

           # get_data(host, db, user, password, id_numerico)->{"data": df -> data to  learn,
           #  "ind_proyeccion": pr_time -> time to forecast}
