import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.stattools import adfuller, kpss
import numpy as np
import scipy.stats as stats
from pmdarima.arima import auto_arima


class model :
    def __init__(self,data, auto: bool,spec: list,season: bool):
        self.zt = data
        self.auto = auto
        self.spec = spec
        self.season = season

## pensarán en especificar o querran la estimacion directo?
## vamos a dejar que sea customisable si queremos directo el pronostico o queremos activarlo nosotros
## en cualquier caso queda resuelta la posible customizacion

    def get_arima(self,zt,auto,epec,season):
        if auto :
            self.params= {
                "autoarima":auto,
                "specification": spec,

            }
            max_order= int(2/np.sqrt(len(zt)))
            max_d =2
            seasonal=False
            model_no_season = auto_arima(self.zt,
                                         max_p= self.max_order,
                                         max_q = self.max_order,
                                         max_d=self.max_d,
                                         seasonal = self.seasonal,
                                         trace=True,
                                         error_action='ignore',
                                         suppress_warnings=True,
                                         stepwise=True)
            self.no_season = model_no_season
            model_season = auto_arima(self.zt,
                                         max_p=self.max_order,
                                         max_q=self.max_order,
                                         max_d=self.max_d,
                                         seasonal=self.seasonal,
                                         m=12,
                                         trace=True,
                                         error_action='ignore',
                                         suppress_warnings=True,
                                         stepwise=True)
            self.season = model_season
        else:
            if len(self.spec)>0:
                try:
                    if self.season:
                       season_model= auto_arima(self.zt,
                                   p = self.spec[0],
                                   d = self.spec[1],
                                   q = self.spec[2],
                                   seasonal = season,
                                   m = 12

                        )
                    else:
                        season_model = auto_arima(self.zt,
                                                  p=self.spec[0],
                                                  d=self.spec[1],
                                                  q=self.spec[2],
                                                  seasonal=season,
                                                  m=12
                                                  )
                except:
                    print(f"parameter set wornglty setted {self.params}")





