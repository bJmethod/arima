
## devuelve un diccionario con las credenciales. con la estructura
## {"usr": "xxx", password: "yyyy"}
import configparser
def sensitive_dict():
    config = configparser.ConfigParser()
    config.read('C:/Users/Usuario/Documents/projects/arima/config.ini')
    database_host = config['DEFAULT']['HOST']
    database_puerto = config['DEFAULT']['PORT']
    database_base = config['DEFAULT']['DB']
    database_usuario = config['DEFAULT']['USER']
    database_password = config['DEFAULT']['PASSWORD']

    configuraciones = {"usr": database_usuario, "password": database_password, "host" : database_host, "puerto" : database_puerto, "db" : database_base}
    return configuraciones


