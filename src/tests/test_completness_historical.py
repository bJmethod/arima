import unittest
from src.resources.create_study_Case import *
from src.db_connections import *
import pandas as pd

class testCompleteness(unittest.TestCase):

    def testHistoricalData(self):
        file = './resources/test_10431.csv'
        df = pd.read_csv(file)
        df.rename(columns={ "historicoporccomp":"valor" , "anionro":"anio", "historicomes":"mes"}, inplace=True)
        inicio= df.anio.min()
        fin = df.anio.max()
        expected_periods = (fin -inicio+1 )*18
        new = complete_series( inicio, fin, df)
        actual_periods= len(new)
        #print(f"which months {which_months}")
        #valores = createStudycase(file)
        self.assertEquals(expected_periods, actual_periods)

    def testUpdateMonthsConstantForecastCase(self):
        pass
    def testCasetoFail(self):
        file = './resources/caso_prueba_1.csv'
        createStudycase(file,1)
        pass
    def testCasetoFail2(self):
        file = './resources/caso_prueba_2.csv'
        createStudycase(file,1)
        pass

    def testCasetoFail3(self):
        file = './resources/prueba_problemas.csv'
        createStudycase(file, 1)
        pass