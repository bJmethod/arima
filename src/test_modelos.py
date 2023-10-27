import unittest
import main

class TestModelos(unittest.TestCase):

## TO-DO arreglar test de error y arreglar clase de forecast

    def test_forecast_error(self):
        serie = [1,1,1,1,1,1,1,1,1,]
        modelo = main.model(serie, True, [], False)
        modelo.get_arima()
        forecast = modelo.forecast()
        self.assertEquals(forecast, "error")

