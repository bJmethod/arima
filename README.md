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

## TODO: agregar esquema basico

## TODO: agregar plug para conceccion a base de datos


## TODO: Agregar test unitarios
