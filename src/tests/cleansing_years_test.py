import unittest
from src.resources.create_study_Case import *
from src.db_connections import *
import pandas as pd


class testCleansingYears(unittest.TestCase):

    def testClensingYears(self):
        file = './resources/Problema1.csv'
        df = pd.read_csv(file)
        df.rename(columns={"porcentaje":"valor"}, inplace=True)
        cleaning_years = excluir_anio_credito(df, 1,2,'conn')
        years_excluded = cleaning_years["years_excluded"]

        self.assertEquals(2021,years_excluded[0])


    def testCleanedData(self):
        file = './resources/Problema1.csv'
        df = pd.read_csv(file)
        df.rename(columns={"porcentaje":"valor"}, inplace=True)
        cleaning_years = excluir_anio_credito(df, 1,2,'conn')
        data_cleaned = cleaning_years["cleaned_df"]
        stats = data_cleaned.valor.describe()
        self.assertIsNot(100,stats["min"])
        self.assertIsNot(10000,stats["max"])

    def testForecastWithClenedData(self):
        from src.model import model
        from src.utils import integrate_series

        file = './resources/Problema1.csv'
        df = pd.read_csv(file)
        df.rename(columns={"porcentaje":"valor"}, inplace=True)
        cleaning_years = excluir_anio_credito(df, 1,2,'conn')
        data_cleaned = cleaning_years["cleaned_df"]
        Xt = data_cleaned["valor"]

        model = model(Xt, True, [], True)
        model.get_arima()
        model.forecast(18)
        valoresD = model.predictions
        valores = integrate_series(valoresD)
        min_f =min(valores)
        max_f = max(valores)
        self.assertTrue(min_f<100)
        self.assertTrue(max_f > min_f)