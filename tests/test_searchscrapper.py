import unittest
import jacksoncountydeedsearchscrapper
import time
from model.lot import Lot
from model.record import Record
import datetime


class Test_Search_Scrapper(unittest.TestCase):

    _url = "http://records.jacksongov.org/RealEstate/SearchEntry.aspx"
    _detail_url = "http://records.jacksongov.org/RealEstate/MiniDetail.aspx?id="



    def test_two_page_retrieval(self):
        scrapper = jacksoncountydeedsearchscrapper.SearchScrapper(Test_Search_Scrapper._url,
                                                                  Test_Search_Scrapper._detail_url, "html5lib")

        scrapper.disclaimer_screen()

        scrapper.search_screen("JENNINGS MANOR", " 29")
        lot = scrapper.parse_data_for_lot("JENNINGS MANORS", "29")

        self.assertEqual(len(lot.get_records), 35)

"""
    def test_single_page_retrieval(self):
        scrapper = jacksoncountydeedsearchscrapper.SearchScrapper(Test_Search_Scrapper._url, Test_Search_Scrapper._detail_url, "html5lib")

        scrapper.disclaimer_screen()
        #scrapper.search_screen("FAR VIEW HEIGHTS", " 1006")
        #lot = scrapper.parse_data_for_lot("FAR VIEW HEIGHTS", "1006")
        
        self.assertEqual(len(lot.get_records),20)

"""
