from bs4 import BeautifulSoup
from bs4.element import Tag
from bs4.element import ResultSet

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

import re
import datetime
import time

from model.record import Record
from model.record import VALID_RECORD_TYPES
from model.lot import Lot

MORE_MEMBERS = "(+)"


class SearchScrapper:
    _DISCLAIMER_ID = 'cph1_lnkAccept'
    _SUBDIVISION_ID = 'cphNoMargin_f_DataTextEdit1'
    _LOT_ID = 'cphNoMargin_f_txtLDSLot'
    _SEARCH_BUTTON_ID = 'cphNoMargin_SearchButtons2_btnSearch'
    _PAGE_sELECT_ID = "cphNoMargin_cphNoMargin_OptionsBar1_ItemList"

    _url: str
    _detail_url: str
    _parser: str
    _html: str
    _driver: webdriver
    _main_tab: str
    _detail_tab: str

    def __init__(self, url: str, detail_url, parser: str = "lxml"):
        self._url = url
        self._detail_url = detail_url
        self._driver = webdriver.Chrome()
        self._parser = parser

        #setup main tab
        self._driver.get("http://www.yahoo.com")
        self._main_tab = self._driver.current_window_handle

        # create second tab to retrieve details
        self._driver.execute_script("window.open('http://www.google.com')")
        WebDriverWait(self._driver, 10).until(EC.number_of_windows_to_be(2))
        tabs_after = self._driver.window_handles
        self._detail_tab = [x for x in tabs_after if x != self._main_tab][0]

        print("exiting SearchScrapper.init")

    def disclaimer_screen(self):
        """
        This method simple clicks a link to get past the disclaimer page.

        :return:
        """
        try:
            self._driver.get(self._url)
            anchor_element = self._driver.find_element_by_id(SearchScrapper._DISCLAIMER_ID)
            anchor_element.click()
        except NoSuchElementException:
            print("anchor link on disclaimer page not found")

    def search_screen(self, subdivision: str, lot: str):
        """
        This method enters in a subdivision and lot to begin retrieving data for

        :param subdivision:
        :param lot:
        :return:
        """

        try:
            self._driver.get(self._url)
            subdivision_input_element = self._driver.find_element_by_id(SearchScrapper._SUBDIVISION_ID)
            subdivision_input_element.send_keys(subdivision)

            lot_input_element = self._driver.find_element_by_id(SearchScrapper._LOT_ID)
            lot_input_element.send_keys(lot)

            search_button_element = self._driver.find_element_by_id(SearchScrapper._SEARCH_BUTTON_ID)
            search_button_element.send_keys('\n')

        except NoSuchElementException:
            print("input elements not found on search page")

    def parse_data_for_lot(self, subdivision: str, lot: str):
        """
        This is the main outer loop that handled calling each page to retrieve data for.

        :return:
        """
        not_finished: bool = True
        current_page: int = 1
        lot = Lot(subdivision, lot)

        total_page_count = self._extract_num_pages()

        #  loop through each page processing records.  If more pages exist navigate to next page and process
        while not_finished:
            records = self._generate_records_list_from_page()
            lot.add_records(records)
            current_page += 1
            if current_page <= total_page_count:
                time.sleep(10)
                self._navigate_to_next_record_list_page(current_page)
            else:
                not_finished = False

        return lot

    def _navigate_to_next_record_list_page(self, current_page):
        """
        This method will determine if this page exists and if so will pull down an update list of records.

        :param current_page:
        :return:
        """

        self._driver.switch_to.window(self._main_tab)
        page_select_tag: Select = Select(self._driver.find_element_by_id(SearchScrapper._PAGE_sELECT_ID))
        page_select_tag.select_by_value(str(current_page))

    def _generate_records_list_from_page(self):
        """
        This method loops through each of the td tags in the table and calls parse row
        to parse the details out of that row.

        :return:
        """
        records: list = []
        table_counter = 0

        soup = BeautifulSoup(self._driver.page_source, self._parser)

        # retrieve data table with id ending with pattern below
        for html_element in soup.find_all("table", {'id': re.compile(r'\S*dataTbl.hdn')}):
            table_counter += 1
            data_table: Tag = html_element

        if table_counter == 1:
            # get each of the rows under the table and process them
            row_counter = 0
            for row_element in data_table.findChildren("tr"):
                if row_counter > 0:
                    record = self._parse_row(row_element)
                    records.append(record)
                row_counter += 1

        elif table_counter == 0:
            print("found no data table element!!!!!!!!!!!!!!")
        else:
            print("found more than one data table element!!!!!")
        return records

    def _parse_row(self, row_element: Tag):
        """
        This method will retrieve all the data from the row.  However, if there are more than one grantee or grantor
        then we will need to call seperate URL to retrieve the complete list of grantees and grantors.  We will do
        this in seperate method after we have retrieved all data for a lot.

        :param row_element:
        :return:
        """

        cell_elements: ResultSet = row_element.findChildren("td")

        county_record_key = cell_elements[23].get_text()
        instrument_num: str = cell_elements[4].get_text()
        date_recorded: datetime.date = datetime.datetime.strptime(cell_elements[8].get_text(), '%m/%d/%Y').date()

        book: str = cell_elements[5].get_text()
        page: str = cell_elements[6].get_text()
        record_type: str = cell_elements[9].get_text()

        if record_type in VALID_RECORD_TYPES:
            record_type: str = cell_elements[9].get_text()
        else:
            print("record_type [" + record_type + "] not in valid list")

        description: str = cell_elements[18].get_text()

        # get Grantors
        grantor_tag = cell_elements[13]
        grantee_tag = cell_elements[16]

        grantors, grantees = self._retrieve_grantors_and_grantees(grantor_tag, grantee_tag, county_record_key)

        record = Record(
            county_record_key,
            instrument_num,
            date_recorded,
            record_type,
            book,
            page,
            grantors,
            grantees,
            description
        )

        return record

    def _retrieve_grantors_and_grantees(self, grantor_tag: Tag, grantee_tag: Tag, county_record_key):
        """
        This method will determine if there is more than one grantee and/or grantor.  If there is only one
        for both it will return.  If there is more than one we will return this so we can mark the record
        for decorating later.

        :param grantor_tag:
        :param grantee_tag:
        :param row_id:
        :return:
        """
        grantors = []
        grantees = []

        # determine if there is more than one grantee
        more_grantees_found = self._check_for_more_members(grantee_tag)

        # determine if there is more than one grantor
        more_grantors_found = self._check_for_more_members(grantor_tag)

        # extract grantees and grantors
        if not more_grantees_found or more_grantors_found:
            # pull grantee and grantor from main table
            grantors = [grantor_tag.get_text()]
            grantees = [grantee_tag.get_text()]
        else:
            grantors, grantees = self._retrieve_grantors_and_grantees_details(county_record_key)

        return grantors, grantees

    def _check_for_more_members(self, tag):
        """"
        check to see if tag indicating more members exist
        """
        more_than_one_found = False

        child_tag = tag.find("b", {"title": "Other Names Indicator"})
        if child_tag is not None:
            child_str: str = child_tag.get_text()
            child_str = child_str.strip()

            if child_str == MORE_MEMBERS:
                more_than_one_found = True
            else:
                print(" found unexpected other name indicator [" + child_str + "]")

        return more_than_one_found

    def _retrieve_grantors_and_grantees_details(self, county_record_key):
        """
        This method will retrieve the detail  record for a single public record
        to retrieve the grantors and grantees

        :param county_record_key:
        :return:
        """
        grantees = []
        grantors = []

        self._driver.switch_to.window(self._detail_tab)

        # Load a page
        self._driver.get(self._detail_url + county_record_key)
        soup = BeautifulSoup(self._driver.page_source, self._parser)

        # retrieve Grantees
        for span_tag in soup.find_all("span", {'id': re.compile(r'lstTees_lblTeeNam_\d+')}):
            grantees.append(span_tag.get_text())

        if len(grantees) < 1:
            print("grantee list should have been 1 or more")

        # retrieve Grantors
        for span_tag in soup.find_all("span", {'id': re.compile(r'lstTors_lblTorNam_\d+')}):
            grantors.append(span_tag.get_text())

        if len(grantors) < 1:
            print("grantor list should have been 1 or more")

        # switch back to main tab
        self._driver.switch_to.window(self._main_tab)

        return grantors, grantees

    def _extract_num_pages(self):
        page_count = 0

        page_select_tag: Select = Select(
            self._driver.find_element_by_id(SearchScrapper._PAGE_sELECT_ID))

        for _ in page_select_tag.options:
            page_count += 1

        print("page count=" + str(page_count))
        return page_count
