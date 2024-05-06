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

def emulate_complete_time_series(df, inicio, fin):
    months_years = find_notFound_month_by_year(df, inicio, fin)
    for year in months_years.keys():
        new = df.copy()
        for month in range(1, 19):
            if month not in new[new.anionro == year].historicomes.unique():
                new = new.append({"anionro": year, "historicomes": month, "valor": None}, ignore_index=True)

    new.index = pd.date_range(start=f"{inicio}-01-01", periods=len(new), freq='M')
    methods = ['linear', 'time', 'quadratic', 'cubic', 'slinear', 'akima', 'polynomial', 'spline']
    results = []
    new['valor'].fillna(new['valor'].mean(), inplace=True)
    for method in methods:
        if method == 'polynomial' or method == 'spline':
            new['Interpolate' + method] = new['valor'].interpolate(method=method, order=3)
        else:
            new['Interpolate' + method] = new['valor'].interpolate(method=method)
        mse = mean_squared_error(new['valor'], new['Interpolate' + method])
        results.append((method, mse))

    best_method, min_mse = min(results, key=lambda x: x[1])

    new["valor"]=new[f"Interpolate{best_method}"]
    return new


def integrate_series(signal):
    for period in range(len(signal)):
        if period % 18 - 1 < 0:
            signal[period] = 0
        else:
            signal[period] = (signal[period] + signal[period - 1])
    return signal
