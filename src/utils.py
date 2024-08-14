import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error
def interpret_steps(aniodesde, aniohasta):
    steps_ahead = int((aniohasta - aniodesde + 1) * 18)
    return {"steps": steps_ahead, "anio_desde": aniodesde}


def interpret_months(i: int):
    return int((i) % 18 + 1)


def interpret_year(anio: int, i: int):
    return int(anio + i // 18)


### is uncomplete time series
def find_notFound_month_by_year(df, inicio, fin):
    which_years = [i for i in range(inicio, fin + 1) if i not in df.anionro.unique()]
    missing_p = dict()
    for year in which_years:
        missing_p[year] = [i for i in range(1, 19) if i not in df[df.anionro == year].historicomes.unique()]

    return missing_p


## ahora recibimos la serie y extraemos el ultimo valor para el calculo del resultado del proceso
def integrate_series(signal,Xt):
    signal_new= np.zeros(len(signal))
    last_value = Xt.iloc[-1]
    for period in range(len(signal)):
        if period==0:
            signal_new[period] = signal[period]+last_value
        else:
            signal_new[period] = (signal[period] + signal_new[period - 1])
    return signal_new
