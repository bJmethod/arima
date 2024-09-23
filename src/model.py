import logging
import numpy as np
from pmdarima.arima import auto_arima, ARIMA
from pmdarima.arima.utils import nsdiffs


class model:
    def __init__(self, data, auto: bool, spec: list, season: bool):
        self.predictions = None
        self.model_season = None
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
        logging.info("Getting total obs")
        obs = len(self.zt)
        try:
            D = nsdiffs(self.zt, m=18, max_D=1)
        except Exception as e:
            D = 0
        try_season = True if obs > 60 else False
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

    def get_diff_series(self):
        diff = np.zeros(len(self.zt))
        señal = self.zt
        try:
            for i in range(len(señal)):
                if i == 0:
                    diff[i] = np.nan
                else:
                    diff[i] = señal[i] - señal[i - 1]
            return diff[1:]
        except Exception as e:
            print(f"error {e}")
            logging.ERROR(f"error {e}")

    def get_arima(self) -> object:
        self.xt = self.get_diff_series()
        print(f"Generating autoarima with auto={self.auto}")

        if self.auto:
            self.params = {
                "autoarima": self.auto,
                "specification": self.spec,
            }
            D, try_season = self.get_minimum_spec_auto()
            self.max_d = 2
            self.seasonal = False
            self.start = 0
            self.D = D
            logging.info("Estimating seasonal order using Cannova-Hansen test")
            models = []

            if try_season:
                try:
                    model_season = auto_arima(self.xt,
                                              start_p=self.start,
                                              start_q=self.start,
                                              start_P=self.start,
                                              D=self.D,
                                              max_p=self.max_order,
                                              max_q=self.max_order,
                                              max_Q=self.max_order,
                                              max_P=self.max_order,
                                              m=18,
                                              trace=False,
                                              error_action='ignore',
                                              suppress_warnings=True,
                                              stepwise=True)
                    self.model_season = model_season
                    models.append(('season', model_season))
                except Exception as e:
                    self.fail = True
                    logging.ERROR(f"Model with seasonality failed: {e}")

                best_metrics = (np.inf, np.inf, -np.inf)  # Initialize with infinite AIC, BIC, and negative R2
                for name, model in models:
                    aic, bic, r2 = self.evaluate_model(model, self.xt)
                    if (aic, bic, -r2) < best_metrics:
                        best_metrics = (aic, bic, -r2)
                        self.best_model = model
                        best_model_name = name

                logging.info(
                    f"Best model selected: {best_model_name} with metrics AIC={best_metrics[0]}, BIC={best_metrics[1]}, R2={-best_metrics[2]}")

                # Check if the selected best model has (0, 0, 0) order and (0, 0, 0, m) seasonal order
                if self.best_model.order == (0, 0, 0) and self.best_model.seasonal_order == (0, 0, 0, 18):
                    logging.info("Best model has order (0, 0, 0) and seasonal order (0, 0, 0, 18). Retrying with stepwise=False.")
                    try:
                        model_no_stepwise = auto_arima(self.xt,
                                                       start_p=self.start,
                                                       start_q=self.start,
                                                       start_P=self.start,
                                                       D=self.D,
                                                       max_p=3,
                                                       max_q=3,
                                                       max_Q=3,
                                                       max_P=3,
                                                       m=18,
                                                       trace=False,
                                                       error_action='ignore',
                                                       suppress_warnings=True,
                                                       stepwise=False)
                        self.best_model = model_no_stepwise
                        logging.info("Stepwise=False model selected as the best model.")
                    except Exception as e:
                        self.fail = True
                        logging.ERROR(f"Model with stepwise=False failed: {e}")

            else:
                print("Not enough observations or variance to try seasonal specification.")
                self.fail = True
                logging.info(f"Not enough observations {len(self.xt)} to try seasonal specification")
                return True

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
                                                with_intercept=False)
                    else:
                        self.model = auto_arima(self.xt,
                                                p=self.spec[0],
                                                d=self.spec[1],
                                                q=self.spec[2],
                                                seasonal=self.season,
                                                m=12)
                except:
                    print(f"Parameters are incorrectly set: {self.params}")

    def forecast(self, periods: int):
        if not self.fail:
            try:
                order = self.best_model.order
                seasonal_order = self.best_model.seasonal_order
                self.manual = ARIMA(order=order, seasonal_order=seasonal_order, with_intercept=False)
                self.manual.fit(self.xt)

                self.predictions = self.manual.predict(n_periods=periods)
            except Exception as e:
                print("No model was set or the number of periods ahead is inappropriate.")
                logging.error(f"Exception raised: {e}")
                self.predictions = np.array([])
        else:
            print("Model was not set.")
            logging.error("Model was not set.")
            self.predictions = np.array([])
