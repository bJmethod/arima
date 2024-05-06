import unittest
from src.resources.create_study_Case import *
from src.utils import *
import pandas as pd

class testCompleteness(unittest.TestCase):

    def testHistoricalData(self):
        file = './resources/test_10431.csv'
        df = pd.read_csv(file)
        df.rename(columns={ "historicoporccomp":"valor"}, inplace=True)
        inicio= df.anionro.min()
        fin = df.anionro.max()
        expected_periods = (fin -inicio+1 )*18
        actual_periods = len(df)
        new = emulate_complete_time_series(df, inicio, fin)
       # print(f"which months {which_months}")
        #valores = createStudycase(file)
        self.assertEquals(expected_periods, actual_periods)

    def testUpdateMonthsConstantForecastCase(self):
        pass
    def testCasetoFail(self):
        pass
