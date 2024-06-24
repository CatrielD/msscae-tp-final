import data
import unittest
from utils import consecutive_pairs
from data import _year_list_to_str

def test_interface():# (pais: IPais):
    "estaría bueno testear la interfaz, tengo en un proyecto código que hace eso, después lo subo"
    pass

class RandomTests(unittest.TestCase):

    def test_consecutive_pairs(self):
        self.assertEqual(consecutive_pairs([2001]), [(2001, 2001)])
        self.assertEqual(consecutive_pairs([2001,2002]), [(2001, 2002)])
        self.assertEqual(consecutive_pairs([2001,2002,2003]), [(2001, 2003)])
        self.assertEqual(consecutive_pairs([2001,2002,2003,2010]), [(2001, 2003),(2010,2010)])
        self.assertEqual(consecutive_pairs([2001,2002,2003,2010,2020]), [(2001, 2003),(2010,2010),(2020,2020)])
        self.assertEqual(consecutive_pairs([2001,2002,2003,2010,2020,2021]), [(2001, 2003),(2010,2010),(2020,2021)])
        self.assertEqual(consecutive_pairs([2001,2010]), [(2001,2001), (2010, 2010)])


    def test_consecutive_pairs(self):
        self.assertEqual(_year_list_to_str(2001), "2001")
        self.assertIn(_year_list_to_str(2001,2002), ["2001-2002", "2001_2002"])
        self.assertEqual(_year_list_to_str(2001,2002,2003), "2001-2003")
        self.assertEqual(_year_list_to_str(2001,2002,2003,2010), "2001-2003_2010")
        self.assertEqual(_year_list_to_str(2001,2002,2003,2010,2020), "2001-2003_2010_2020")
        self.assertEqual(_year_list_to_str(2001,2002,2003,2010,2020,2021),
                         "2001-2003_2010_2020-2021")
        self.assertEqual(_year_list_to_str(2001,2010), "2001_2010")

  
    def test_data_encode(self): 
        eurl = data.encode_url("https://oec.world/api/olap-proxy/data.jsonrecords",
                               {
                                   "Year": "2018,2019,2020",
                                   "cube": "trade_i_baci_a_92",
                                   "drilldowns": "Exporter Country,Year,HS4",
                                   "measures": "Trade Value",
                                   "token": data.OEC_TOKEN
                               })
        # vemos que la url encodeada sea idéntica a la que sabemos que funciona
        expected = "https://oec.world/api/olap-proxy/data.jsonrecords?Year=2018%2C2019%2C2020&cube=trade_i_baci_a_92&drilldowns=Exporter+Country%2CYear%2CHS4&measures=Trade+Value&token=REPLACE_HERE"
        assert eurl == expected, f"Expected:\n{expected}\ngot:\n{eurl}"


if __name__ == "__main__":
    unittest.main()
