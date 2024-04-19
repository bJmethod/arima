import numpy as np


def interpret_steps(aniodesde, aniohasta):
    steps_ahead = int((aniohasta - aniodesde + 1)*18)
    return {"steps": steps_ahead, "anio_desde": aniodesde}

def interpret_months(i: int):
   return int((i) % 18 + 1)

def interpret_year(anio: int,i: int):
    return int(anio + i // 18)

def integrate_series(signal):
    for period in range(len(signal)):
        if period%18 -1 < 0:
            signal[period] = 0
        else:
            signal[period]= (signal[period]+signal[period-1])
    return signal