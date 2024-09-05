import pandas as pd
from sqlalchemy import create_engine
import psycopg2
import logging
from datetime import datetime
from src.utils import *


def upd_procesado(conn, id_numerico, indice) -> object:
    sql_procesado = f""" 
        update confarimamodeloaplicado
        set procesado=TRUE
        where confarimacabezalid={id_numerico} and
        confarimamodeloaplicadoindice= {indice}
        """
    return sql_procesado


def get_to_from(conn, id_numerico) -> object:
    get_to_from_historic_query = f""" 
         select confarimacabezalhistoricodesde as aniodesde, confarimacabezalhistoricohasta as aniohasta
         from confarimacabezal
         where confarimacabezalid= {id_numerico} 
             """
    df = pd.read_sql(get_to_from_historic_query, conn)
    return df


def get_forecast_year(conn, id_numerico) -> object:
    get_to_from_forecast_query = f""" 
        select CONFARIMACABEZALPROYECCIONDESD as aniodesde, CONFARIMACABEZALPROYECCIONHAST as aniohasta
        from confarimacabezal
        where confarimacabezalid= {id_numerico} 
            """

    df = pd.read_sql(get_to_from_forecast_query, conn)
    return df


def get_data_forecast(conn, anio_desde, anio_hasta, indice):
    get_data_query = f"""
            SELECT anionro AS anio, HISTORICOMES AS mes, historicoporccomp AS valor  
            FROM HISTORICO WHERE anionro >= {anio_desde} AND anionro <= {anio_hasta} AND HISTORICOINDICE = {indice}
            AND anionro IN (SELECT anionro FROM HISTORICO WHERE HISTORICOINDICE = {indice} GROUP BY anionro
                            HAVING SUM(CASE WHEN HISTORICOMES = 18 THEN 1 ELSE 0 END) > 0 )
            ORDER BY   anio, mes;
            """
    df = pd.read_sql(get_data_query, conn)

    return df


def update_model_spec_query(valor_ar, valor_i, valor_ma, id_numerico, indice) -> str:
    query = f'''
    update confarimaresultado set confarimaar={valor_ar},
    confarimai= {valor_i}, confarimama= {valor_ma}
    where  confarimacabezalid= {id_numerico} and
    confarimaindice= {indice}
    '''
    return query


def update_valor_forecast(valor, id_numerico, indice, anio, mes) -> str:
    query = f''' 
        update confarimamodeloaplicado
        set procesado=TRUE,
        confarimamodeloaplicadoporc={valor}
        where confarimacabezalid={id_numerico} and
        confarimamodeloaplicadoindice= {indice}
        and confarimamodeloaplicadoanio = {anio} and confarimamodeloaplicadomes = {mes}

    '''

    # print(f"update_valor_forecast={query}")
    return query


def get_conn(host, db, user, password, port):
    print("Conectando a BD..")

    try:

        conexion = psycopg2.connect(host=host, database=db, user=user, password=password, port=port)
        insert_log(conexion, 0, 0, 'db_connections.py',
                   'Conectamos a BD, ' + str(host) + '  ' + str(db) + '  ' + str(user) + '  ' + str(port))
        logging.info(f"Conectamos a BD, {host} {db} {user} {port}")
    except Exception as e:
        print("cant coneect exception {e}")
        logging.ERROR(f"cant coneect exception {e}")

        conexion = None
    return conexion


def get_engine(conn):
    try:
        engine = create_engine('postgresql+psycopg2://', creator=lambda: conn)
    except Exception as e:
        # logging.ERROR(f"can´t create engine {e}")
        insert_log(conn, 0, 0, 'db_connections.py', 'No se puede crear engine ' + str(e))
        logging.ERROR('No se puede crear engine ' + str(e))
        engine = None
    return engine


# metodo que excluye año sin credito
# cuando el maximo mes de un año no tiene credito, se excluye el año
# verificar presencia de valores extremos
# Verificar que ocurran 5 meses de un añ0
#  caso afirmativo excluimos el año
def excluir_anio_credito(df:pd.DataFrame,indice,id_numerico,conexionbd) -> object:
    df = df.copy()

    df['valor'] = df['valor'].astype(float)
    df['anio'] = df['anio'].astype(int)
    df['mes'] = df['mes'].astype(int)
    stats_by_month = df[["anio", "valor"]].groupby('anio').describe()
    stats_by_month = stats_by_month.reset_index()
    stats_by_month.columns= [ 'anio','count','mean','min','std','25%','50%','75%','max']
    years_to_exclude = list(stats_by_month.loc[stats_by_month["50%"]>300,"anio"].values)
    result = df[~df.anio.isin(years_to_exclude)].copy()
    print(f"excluyendo los años sin credito {years_to_exclude} para el inidice {indice} y el id {id_numerico}")
    #logging.info(f"excluyendo los años sin credito {years_to_exclude} para el inidice {indice} y el id {id_numerico}")
  #  insert_log(conexionbd, id_numerico,indice, 'db_connections.py', f"excluyendo los años sin credito {years_to_exclude} para el inidice {indice} el id {id_numerico}")
    # excluye años con valores extremos
    return {"cleaned_df":result, "years_excluded":years_to_exclude}


def get_data(conexionbd, conn, id_numerico, indice):
    print(f'getting data for {id_numerico}')
    insert_log(conexionbd, id_numerico, indice, 'db_connections.py', 'Obtener datos para id=' + str(id_numerico))

    forecast_year = get_to_from(conn, id_numerico)  # GABRIEL de aca se saca desde y hasta a tomar del historico
    # forecast_year -> {"aniodesde":[1],"aniohasta":[2]}
    anio_desde = forecast_year.aniodesde[0]
    anio_hasta = forecast_year.aniohasta[0]
    logging.info(f"anio_desde historico = {anio_desde}")
    logging.info(f"anio_hasta historico = {anio_hasta}")
    insert_log(conexionbd, id_numerico, indice,'db_connections.py', 'historico anio_desde = '+str(anio_desde)+' anio_hasta = '+str(anio_hasta))

    df = get_data_forecast(conn, anio_desde, anio_hasta,
                           indice)  ## GABRIEL se pasa indice para obtener los datos del historico
    ## aqui tengo que agregar el metodo que excluya el año cuando no tenga credito



    insert_log(conexionbd, id_numerico, indice, 'db_connections.py',
               'Fin get dato anio_desde = ' + str(anio_desde) + ' anio_hasta = ' + str(anio_hasta) + ' indice ' + str(
                   indice))
    logging.info(f'finishing geting data {anio_desde} {anio_hasta} and indice {indice}')
    # df tiene N anos y N meses, pero puede que no este completo (N anos*18)
    # Create a DataFrame with all possible combinations of years and months
    #df2 = complete_series(anio_desde, anio_hasta, df)
    # despues de completar la serie, se excluyen los años sin credito
    #df2 = excluir_anio_credito(df2, indice, id_numerico, conexionbd)["cleaned_df"]
    pr_time = get_forecast_year(conn, id_numerico)
    to_log = [pr_time, df]
    str_case = ["Anios para forecast= ","Agregado de 0= "]

    for i in range(2):
        json_str = to_log[i].to_json(orient='records', lines=True)
        insert_log(conexionbd, id_numerico, indice, 'db_connections.py', f'{str_case[i]}' + str(json_str))
        logging.info(f'{str_case[i]}' + str(json_str))
    return {"data": df,
            "ind_proyeccion": pr_time}


def complete_series(anio_desde, anio_hasta, df):
    df2 = pd.DataFrame([(year, month, 0) for year in range(anio_desde, anio_hasta + 1) for month in range(1, 19)],
                       columns=['anio', 'mes', 'valor'])
    # Update 'valor' column in df2 based on the values in df
    df2.set_index(['anio', 'mes'], inplace=True)
    df.set_index(['anio', 'mes'], inplace=True)
    df2.update(df)
    df2.reset_index(inplace=True)
    return df2


def __do_update(conn, query, id_numerico, indice, type):
    cur = conn.cursor()
    logging.info(f'updating with {query} for {id_numerico}')
    insert_log(conn, id_numerico, indice, 'db_connections.py', 'Update (' + str(type) + ')= ' + str(query))
    cur.execute(query)
    conn.commit()
    logging.info(f"updated {type} {id_numerico}")
    logging.info(f" update query {query}")

def load_forecast_info(conn, id_numerico: int, valor_ar: int, valor_i: int, valor_ma: int, indice: str):
    update_espec_query = update_model_spec_query(valor_ar, valor_i, valor_ma, id_numerico, indice)
    __do_update(conn, update_espec_query, id_numerico, indice, 'specs')
    insert_log(conn, id_numerico, indice, 'db_connections.py',
               'Fin load del modelo ' + str(id_numerico) + ' - ' + str(indice))
    logging.info(f"finish load model info for {id_numerico} - {indice}")


def load_forecast_values(conn, id_numerico: int, indice: str, valores: list, anio, ):
    for i, l in enumerate(valores):
        m = interpret_months(i)
        valor = round(valores[i], 3)
        anio_actual = interpret_year(anio, i)
        insert_log(conn, id_numerico, indice, 'db_connections.py',
                   'Actualizando porc: ' + str(id_numerico) + ' - ' + str(indice) + ' - ' + str(
                       anio_actual) + ' - ' + str(m) + ' = ' + str(valor))
        query_update_forcast = update_valor_forecast(valor, id_numerico, indice, anio_actual, mes=m)
        __do_update(conn, query_update_forcast, id_numerico, indice, 'update_forecast')


def insert_log(conn, id_numerico: str, indice: str, programa: str, textolog: str):
    ahora = datetime.now()
    fecha_hora_formato = ahora.strftime("%Y-%m-%d %H:%M:%S")
    texto = str(id_numerico) + '-' + str(indice) + '--python'
    query = f'''
    INSERT INTO log (logfecha, logversion, logusuario, logprograma, logdescripcion) VALUES 
    ('{fecha_hora_formato}', '1', '{texto}', '{programa}', '{textolog}');
    '''
    #cur = conn.cursor()
    #cur.execute(query)
    #conn.commit()
    #logging.info( f"{texto}")