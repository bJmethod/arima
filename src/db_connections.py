import psycopg2

HOST= "host"
DB= "db"
USER = "user"
PASSWORD= "pss"
id_numerico = 21
conexion = psycopg2.connect(host=HOST, database=DB, user=USER, password=PASSWORD)

anio_desde = 21
anio_hasta= 21


get_to_from_historic_query = f""" 
    select confarimacabezalhistoricodesde as aniodesde, confarimacabezalhistoricohasta as aniohasta
    from confarimacabezal
    where confarimacabezalid= {id_numerico} 
        """

get_to_from_forecast_query = f""" 
    select confarimacabezalproyecciondesde as aniodesde, confarimacabezalproyeccionricohasta as aniohasta
    from confarimacabezal
    where confarimacabezalid= {id_numerico} 
        """

get_data_query = f""""
        select anionro as anio, datoshistoricoejincmes as mes, datoshistoricoejinccredvi as valor
        from datoshistoricoejinc
        where anionro >= {anio_desde} and anionro<= {anio_hasta} and datoshistoricoejincindice = {id_numerico}
        """


def get_to_from(query,conn):
    cur = conn.cursor()
    cur.execute(query)

