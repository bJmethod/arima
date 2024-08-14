# arima

Proyecto Python

. Recibe por parametros la unidad 

. Recibe por parametros la especificacion ARIMA(P,D,Q) 

. Retorna un csv con un pronostico 18 periodos Para Adelante



## clase model

si se especifica auto= True estima el mejor arima
automaticamente,

Elige entre el mejor modelo SARIMA y el mejor modelo ARIMA,
seleccionando el de mas bajo AIC


se instancia pasandole :
data:  una pd serie, auto: booleano,
spec:una lista que especifica el orden de la serie
si auto = True no hay que proporcionarla,
season: bool

## version 18_07_2024

Lo nuevo:
En  db_connections
Agregamos el metodo excluir_anio_credito, busca años con valores atpicos tales que su masa afecte la mediana, 
estos años suelen ser aquellos que afectan el resultado del modelo,
los excluye cuando lo invoca get_data  y loggea el resultado de los años excluidos por tupla.

En model dejamos libre la busqueda de los parametros AR MA.

## version 13_08_2024

En esta version corregimos bug en diferencias de la serie,
en el metodo get_diff_series de la clase model,

tambien corregimos el metodo integrate_series ahora recibe el vectore de valores y se queda con el ultimo
para aplicar el incremento.

Agregamos la estimacion demodelo sin termino independiente tomando la mejor especificacion determinada por autoarima
y realizando una estimacion del mejor arima encontrado sin ordenada al origen.

