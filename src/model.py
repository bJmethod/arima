import logging
import numpy as np
import pandas as pd
from pmdarima.arima import auto_arima, ARIMA
from pmdarima.arima.utils import nsdiffs



class model:
    def __init__(self, data, auto: bool, spec: list, season: bool):
        self.predictions = None
        self.model_season = None
        self.no_season = None
        self.D = None
        self.start = None
        self.seasonal = None
        self.params = None
        self.max_d = None
        self.max_order = None
        self.zt = data.fillna(method='backfill')
        self.auto = auto
        self.spec = spec
        self.season = season
        self.fail = False
        self.best_model = None


    def get_minimum_spec_auto(self):
        logging.info("geting total obs")
        cases = len(self.zt.unique())
        obs = len(self.zt)
        D = nsdiffs(self.zt, m=18, max_D=2) if cases > 30 else 0
        try_season = True if obs > 30 else False
        return D, try_season

    def calculate_r2(self, y_true, y_pred):
        ss_total = np.sum((y_true - np.mean(y_true)) ** 2)
        ss_residual = np.sum((y_true - y_pred) ** 2)
        r2 = 1 - (ss_residual / ss_total)
        return r2

    def evaluate_model(self, model, actual):
        aic = model.aic()
        bic = model.bic()
        predictions = model.predict_in_sample()
        r2 = self.calculate_r2(actual, predictions)
        return aic, bic, r2

## fixeado bug que diferenciaba solo hasta 18 y volvia
    def get_diff_series(self):
        diff = np.zeros(len(self.zt))
        # take series and return the diff vs previous perio# d
        señal = self.zt
        try:
            for i in range( len(señal)):
                #modulus function  from i to 18

                if i == 0:
                    diff[i] = np.nan
                else:
                    diff[i] = señal[i] - señal[i - 1]
            return  diff[1:]
        except Exception as e:
            print(f"error {e}")
            logging.ERROR(f"error {e}")



    def get_arima(self) -> object:
        self.xt = self.get_diff_series()
        print(f" generating autoarima{self.auto}")
        if self.auto:
            self.params = {
                "autoarima": self.auto,
                "specification": self.spec,

            }
            D, try_season = self.get_minimum_spec_auto()
            self.max_d = 2
            self.seasonal = False
            self.start = 1
            self.D = D
            logging.info(f"estimating seasonal order using cannova-hansen test")
            models = []
            try:
                logging.info("estimating arima no season ")
                model_no_season = auto_arima(self.xt, start_p=self.start, start_q=self.start,
                                            # orden de ar y ma libre
                                             max_p=None, max_q=None,
                                             seasonal=self.seasonal,
                                             trace=False,
                                             error_action='ignore',
                                             suppress_warnings=True,
                                             stepwise=True,
                                            trend = None
                )
                self.no_season = model_no_season
                models.append(('no_season', model_no_season))
            except Exception as e:
                self.fail= True
                logging.ERROR(f"model with no season was failed with exception {e}")

            ## podemos agregar la estimacion de D con el metodo de canova

            ## revisar aqui por qué rompe,
            if try_season:
                try:
                    model_season = auto_arima(self.xt,
                                              start_p=self.start,
                                              start_q=self.start,
                                              start_P=self.start,
                                              D=self.D,
                                              max_p=None,
                                              max_q=None,
                                              m=18,
                                              trace=False,
                                              error_action='ignore',
                                              suppress_warnings=True,
                                              stepwise=True,
                                              trend=None

                    )
                    self.model_season = model_season
                    models.append(('season', model_season))
                except Exception as e:
                    self.fail = True
                    logging.ERROR(f"model with season has failed {e}")
                best_metrics = (
                np.inf, np.inf, -np.inf)  # Initialize with infinite AIC and BIC, and negative infinite R2
                for name, model in models:
                    aic, bic, r2 = self.evaluate_model(model, self.xt)
                    if (aic, bic, -r2) < best_metrics:
                        best_metrics = (aic, bic, -r2)
                        self.best_model = model
                        best_model_name = name

                logging.info(
                    f"Best model selected: {best_model_name} with metrics AIC={best_metrics[0]}, BIC={best_metrics[1]}, R2={-best_metrics[2]}")
            else:
                print("model hasn't enought obs or variance to try seasonal spec")
                logging.info(f"model hasn't enought obs {len(self.xt)} to try seasnal spec")

        else:
            if len(self.spec) > 0:
                try:
                    if self.season:
                        self.model = auto_arima(self.xt,
                                                p=self.spec[0],
                                                d=self.spec[1],
                                                q=self.spec[2],
                                                seasonal=self.season,
                                                m=18,
                                                with_intercept=False

                                                )


                    else:
                        self.model = auto_arima(self.xt,
                                                p=self.spec[0],
                                                d=self.spec[1],
                                                q=self.spec[2],
                                                seasonal=self.season,
                                                m=12
                                                )
                except:
                    print(f"parameter are wrongly setted {self.params}")

    def forecast(self, periods: int):
        if not self.fail:
            try:
                order = self.best_model.order
                seasonal_order = self.best_model.seasonal_order
                ## forzamos estimacion de proceso arima sin intercepto
                self.manual = ARIMA(order=order, seasonal_order=seasonal_order,with_intercept=False)
                self.manual.fit(self.xt)

                self.predictions = self.manual.predict(
                    n_periods=periods
                )
            except Exception as e:
                print("no model was set or n periods ahead are unapropriate ")
                logging.ERROR(f"exception raise {e}")
        else:
            print("model was not setted")
            logging.ERROR("model was not setted")
