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
        file = './resources/historico_2955.csv'
        indice= 1
        valores = createStudycase(file,indice)
        month_to_insert = [interpret_months(i) for i, l in enumerate(valores)]
        expected = [i + 1 for i in range(18)]
        for i, l in enumerate(valores):
            m = interpret_months(i)
            print(f"inserting the month {m}")
        self.assertEquals(month_to_insert, expected)

    def testFakeInserts(self):
        file = './resources/historico_2955.csv'
        indice= 1
        valores = createStudycase(file, indice)
        fake_id = '12'
        expected = [update_valor_forecast(1, fake_id, indice, 2024, mes=m+1) for m in range(18)]
        test_inserts = []
        for i, l in enumerate(valores):
            m = interpret_months(i)
            test_inserts.append(update_valor_forecast(1, fake_id, indice, 2024, mes=m))
        self.assertEquals(test_inserts, expected)

    def testError(self):
        file = './resources/historico_856.csv'
        indice= 1
        valores = createStudycase(file, indice)
        expected_values = [98.203997,
        96.813157,
        96.798174,
        96.932305,
        96.888032,
        97.053055,
        97.260635,
        97.279702,
        97.242942,
        97.247691,
        97.237864,
        97.209697,
        97.202998,
        97.209794,
        97.210413,
        97.210107,
        97.213433,
        97.215035]
        print(valores)
        test_list = [round(num, 6) for num in list(valores)]
        self.assertListEqual(test_list,expected_values )

