import psycopg2

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
    cur = conn.cursor()
    cur.execute(get_to_from_historic_query)
def get_forecast_year(conn,id_numerico):
    get_to_from_forecast_query = f""" 
        select confarimacabezalproyecciondesde as aniodesde, confarimacabezalproyeccionricohasta as aniohasta
        from confarimacabezal
        where confarimacabezalid= {id_numerico} 
            """
    cur = conn.cursor()
    cur.execute(get_to_from_forecast_query)
def get_data_forecast(conn,anio_desde, anio_hasta,id_numerico ):
    get_data_query = f""""
            select anionro as anio, datoshistoricoejincmes as mes, datoshistoricoejinccredvi as valor
            from datoshistoricoejinc
            where anionro >= {anio_desde} and anionro<= {anio_hasta} and datoshistoricoejincindice = {id_numerico}
            """
    cur = conn.cursor()
    cur.execute(get_data_query)

def get_conn(host, db, user, password):
    print("conecting to db..")
    conexion = psycopg2.connect(host=host, database=db, user=user, password=password)
    return conexion

def get_data(host, db, user, password, id_numerico):
    conn = get_conn(host, db, user, password)
    forecast_year = get_forecast_year(conn, id_numerico)
    anio_desde= forecast_year[0]
    anio_hasta = forecast_year[1]
    return get_data_forecast(conn, anio_desde, anio_hasta, id_numerico)
