from src.model import model
import numpy as np
import pandas as pd
from src.utils import *
from src.db_connections import *

def createStudycase(file: str, inidce: int) -> list:
    anio_desde =2024
    anio_hasta= 2024
    study_case = pd.read_csv(file)
    study_case.rename(columns ={'historicoporccomp':"valor"},inplace=True)
    steps_interpreted = interpret_steps(anio_desde, anio_hasta)
    steps = steps_interpreted["steps"]
    X = study_case["valor"]
    arima = model(X, True, [], False)
    arima.get_arima()
    arima.forecast(int(steps))
    valores = arima.predictions
    return valores

