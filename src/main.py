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

## to - do falta metodo que compare las metricas de los dos mejores autoarima y elija el mejor de los dos
    
    def get_arima(self):
        if self.auto :
            self.params= {
                "autoarima": self.auto,
                "specification": self.spec,

            }
            self.max_order= int(2/np.sqrt(len(self.zt)))
            self.max_d =2
            self.seasonal=False
            self.start = 1
            self.D = 0
            model_no_season = auto_arima(self.zt,
                                         start_p=self.start,
                                         start_q=self.start,
                                         start_P=self.start,
                                         max_p= self.max_order,
                                         max_q = self.max_order,
                                         max_d=self.max_d,
                                         D=self.D,
                                         seasonal = self.seasonal,
                                         trace=True,
                                         error_action='ignore',
                                         suppress_warnings=True,
                                         stepwise=True)
            self.no_season = model_no_season
            model_season = auto_arima(self.zt,
                                        start_p=self.start,
                                        start_q=self.start,
                                        start_P=self.start,
                                        D=self.D,
                                        max_p=self.max_order,
                                        max_q=self.max_order,
                                        max_d=self.max_d,
                                        seasonal=self.seasonal,
                                         m=12,
                                         trace=True,
                                         error_action='ignore',
                                         suppress_warnings=True,
                                         stepwise=True)
            self.model_season = model_season

            aic_season = self.model_season.aic()
            aic_no_season = self.no_season.aic()
            if aic_season > aic_no_season:
                self.model = self.model_season
            else:
                self.model = self.no_season
        else:
            if len(self.spec)>0:
                try:
                    if self.season:
                       self.season_model= auto_arima(self.zt,
                                   p = self.spec[0],
                                   d = self.spec[1],
                                   q = self.spec[2],
                                   seasonal = self.season,
                                   m = 12

                        )
                    else:
                        self.season_model = auto_arima(self.zt,
                                                  p=self.spec[0],
                                                  d=self.spec[1],
                                                  q=self.spec[2],
                                                  seasonal=self.season,
                                                  m=12
                                                  )
                except:
                    print(f"parameter set wornglty setted {self.params}")



if __name__== "__main__":
    df = pd.read_excel("C:/Users/Usuario/Documents/Arima.xlsx",skiprows= 1)
    Xt = df[['Ejecución Comprometida']].copy()
    Xt.rename(columns={'Ejecución Comprometida': 'ejec_cp'}, inplace=True)

    model = model(Xt,"true",[],False)

    a = 1
    model.get_arima()
    a +=1

