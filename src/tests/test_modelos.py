import unittest
from src.model import model
import numpy as np

class TestModelos(unittest.TestCase):
    def test_forecast_error(self):
        serie = [1,1,1,1,1,1,1,1,1,]
        modelo = model(serie, True, [], False)
        modelo.get_arima()
        modelo.forecast(periods = 2)
        forecast = modelo.predictions
        self.assertEquals(forecast[0],np.array([float(0)]) )
        print ("estimated model")