import unittest
from src.resources.create_study_Case import *
from src.db_connections import *


class Testupdates(unittest.TestCase):

    def testUpdateMessages(self):
        file = './resources/historico_9.xlsx'
        valores = createStudycase(file)
        month_to_insert = [interpret_months(i) for i, l in enumerate(valores)]
        expected = [i + 1 for i in range(18)]
        print(f"actual months{str(month_to_insert)}")
        print (f"expected {str(expected)}")
        self.assertEquals(month_to_insert, expected)

    def testUpdateMonthsConstantForecastCase(self):
        valores = [18]*18
        expected = [i + 1 for i in range(18)]
        month_to_insert = [interpret_months(i) for i, l in enumerate(valores)]
        self.assertEquals(month_to_insert, expected)

    def testCasetoFail(self):
        valores = [
            75.862, 75.862, 75.862, 75.862, 75.862, 75.862, 75.862, 75.862,  75.862, 75.862, 75.862, 75.862,
             75.862, 75.862, 75.862, 75.862, 75.862,75.862
        ]
        expected = [i + 1 for i in range(18)]
        month_to_insert = [interpret_months(i) for i, l in enumerate(valores)]
        self.assertEquals(month_to_insert, expected)


    def testInsertionMessages(self):
        file = './resources/historico_12125.csv'
        indice= 1
        valores = createStudycase(file,indice)
        month_to_insert = [interpret_months(i) for i, l in enumerate(valores)]
        expected = [i + 1 for i in range(18)]
        for i, l in enumerate(valores):
            m = interpret_months(i)
            print(f"inserting the month {m}")
        self.assertEquals(month_to_insert, expected)

    def testFakeInserts(self):
        file = './resources/historico_13764.csv'
        indice= 1
        valores = createStudycase(file, indice)
        fake_id = '12'
        expected = [update_valor_forecast(1, fake_id, indice, 2024, mes=m+1) for m in range(18)]
        test_inserts = []
        for i, l in enumerate(valores):
            m = interpret_months(i)
            test_inserts.append(update_valor_forecast(1, fake_id, indice, 2024, mes=m))
        self.assertEquals(test_inserts, expected)