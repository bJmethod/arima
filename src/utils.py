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



def integrate_series(signal):
    signal_new= np.zeros(len(signal))
    for period in range(len(signal)):
        if period % 18 - 1 < 0:
            signal_new[period] = signal[period]
        else:
            signal_new[period] = (signal[period] + signal_new[period - 1])
    return signal_new
