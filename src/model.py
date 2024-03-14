import logging
import numpy as np
from pmdarima.arima import auto_arima
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
        self.zt = data
        self.auto = auto
        self.spec = spec
        self.season = season

    def get_minimum_spec_auto(self):
        logging.info("geting total obs")
        cases = len(self.zt.unique())
        obs =  len(self.zt)
        D = nsdiffs(self.zt, m=12, max_D=2) if cases > 30 else 0
        try_season = True if obs > 30 else False
        return D, try_season


    def get_arima(self) -> object:

        print(f" generating autoarima{self.auto}")
        if self.auto:
            self.params = {
                "autoarima": self.auto,
                "specification": self.spec,

            }
            D, try_season = self.get_minimum_spec_auto()
            self.max_order = 4
            self.max_d = 2
            self.seasonal = False
            self.start = 1
            self.D =D
            logging.info(f"estimating seasonal order using cannova-hansen test")


            try:
                logging.info("estimating arima no season ")
                model_no_season = auto_arima(self.zt, start_p=self.start, start_q=self.start,
                                             max_p=self.max_order, max_q=self.max_order,
                                             seasonal=self.seasonal,
                                             trace=True,
                                             error_action='ignore',
                                             suppress_warnings=True,
                                             stepwise=True)
                self.no_season = model_no_season
            except Exception as e:
                logging.ERROR(f"model with no season was failed with exception {e}")

            ## podemos agregar la estimacion de D con el metodo de canova

            ## revisar aqui por qué rompe,
            if try_season:
                try:
                    model_season = auto_arima(self.zt,
                                              start_p=self.start,
                                              start_q=self.start,
                                              start_P=self.start,
                                              D=self.D,
                                              max_p=self.max_order,
                                              max_q=self.max_order,
                                              max_d=self.max_d,
                                              m=12,
                                              trace=True,
                                              error_action='ignore',
                                              suppress_warnings=True,
                                              stepwise=True)
                    self.model_season = model_season
                except Exception as e:
                    logging.ERROR(f"model with season has failed {e}")
                aic_season = self.model_season.aic() if self.model_season else np.inf
            else:
                print("model hasn't enought obs or variance to try seasonal spec")
                logging.info(f"model hasn't enought obs {len(self.zt)} to try seasnal spec")
                aic_season = np.infty
            aic_no_season = self.no_season.aic()
            if aic_season > aic_no_season:
                self.model = self.no_season
                logging.info(f"no season model was selected with aic{aic_no_season}")
            else:
                self.model = self.model_season
                logging.info(f"seasonal model was selected with aic{aic_season}")
        else:
            if len(self.spec) > 0:
                try:
                    if self.season:
                        self.model = auto_arima(self.zt,
                                                p=self.spec[0],
                                                d=self.spec[1],
                                                q=self.spec[2],
                                                seasonal=self.season,
                                                m=12

                                                )


                    else:
                        self.model = auto_arima(self.zt,
                                                p=self.spec[0],
                                                d=self.spec[1],
                                                q=self.spec[2],
                                                seasonal=self.season,
                                                m=12
                                                )
                except:
                    print(f"parameter are wrongly setted {self.params}")

    def forecast(self, periods: int) -> list:
        try:
            self.predictions = self.model.predict(
                n_periods=periods
            )
        except Exception as e:
            print("no model was set or n periods ahead are unapropriate ")
            logging.ERROR(f"exception raise {e}")


