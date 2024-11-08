import datetime

from urllib.parse import urlparse
from urllib.parse import parse_qs

from pydantic import HttpUrl, AnyUrl, BaseModel, PositiveInt

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

from config import settings
from common.services.selenium import TutuParser


class Station(BaseModel):
    title: str
    nnst: PositiveInt
    city: str
    date: str
    time: str


class ShortTrainInfo(BaseModel):
    train_number: str
    trip_time: str
    departure_station: Station
    arrival_station: Station


class TrainInfo(ShortTrainInfo):
    train_page_url: HttpUrl


class TrainsAnswer(BaseModel):
    trains_list: list[TrainInfo]
    wait_list: list[ShortTrainInfo]


class TrainsTutuParser(TutuParser):
    def get_trains_list_by_titles(self,
                                  departure_st: str,
                                  arrival_st: str,
                                  date: datetime.date
                                  ) -> TrainsAnswer:
        self._open_page(AnyUrl(settings.TUTURU_URL.SEARCH_ROUTES_URL))

        departure_station_input = self.__driver.find_element(
            By.XPATH, settings.TUTURU_URL.XPATH.ROUTES_PAGE.DEPARTURE_ST_INPUT)
        arrival_station_input = self.__driver.find_element(
            By.XPATH, settings.TUTURU_URL.XPATH.ROUTES_PAGE.ARRIVAL_ST_INPUT)
        date_input = self.__driver.find_element(
            By.XPATH, settings.TUTURU_URL.XPATH.ROUTES_PAGE.DATE_INPUT)

        departure_station_input.send_keys(departure_st)
        try:
            departure_hinting_element = WebDriverWait(self.__driver, settings.SELENIUM_CONF.PAGE_LOAD_DELAY).until(
                EC.presence_of_element_located(
                    (By.XPATH, settings.TUTURU_URL.XPATH.ROUTES_PAGE.FIRST_DEPARTURE_CITY_HINTING))
            )
        except TimeoutException:
            return TrainsAnswer(trains_list=[], wait_list=[])

        departure_hinting_element.click()

        arrival_station_input.send_keys(arrival_st)
        try:
            arrival_hinting_element = WebDriverWait(self.__driver, settings.SELENIUM_CONF.PAGE_LOAD_DELAY).until(
                EC.presence_of_element_located(
                    (By.XPATH, settings.TUTURU_URL.XPATH.ROUTES_PAGE.FIRST_ARRIVAL_CITY_HINTING))
            )
        except TimeoutException:
            return TrainsAnswer(trains_list=[], wait_list=[])

        arrival_hinting_element.click()

        date_input.send_keys(date.strftime('%d.%m.%Y'))

        show_schedule_button = self.__driver.find_element(
            By.XPATH, settings.TUTURU_URL.XPATH.ROUTES_PAGE.SHOW_SCHEDULE_BUTTON)
        show_schedule_button.click()

        return self._parse_trains_list()

    def get_trains_list_by_nnst(self,
                                nnst1: int,
                                nnst2: int,
                                date: datetime.date
                                ) -> TrainsAnswer:
        url = AnyUrl(settings.TUTURU_URL.SEARCH_TRAINS_URL.format(
            nnst1=nnst1, nnst2=nnst2, date=date.strftime('%d.%m.%Y')
        ))
        self._open_page(url)

        return self._parse_trains_list()

    def _parse_trains_list(self) -> TrainsAnswer:
        try:
            WebDriverWait(self.__driver, settings.SELENIUM_CONF.PAGE_LOAD_DELAY).until(
                EC.presence_of_element_located(
                    (By.XPATH, settings.TUTURU_URL.XPATH.TRAINS_LIST_PAGE.HEADER))
            )
        except TimeoutException:
            return TrainsAnswer(trains_list=[], wait_list=[])

        trains_info_list: list[TrainInfo] = []
        wait_list: list[ShortTrainInfo] = []
        trains_list = self.__driver.find_elements(
            By.XPATH, settings.TUTURU_URL.XPATH.TRAINS_LIST_PAGE.TRAINS_LIST)
        for train in trains_list:
            for _ in range(5):
                try:
                    train_info = self._parse_train(train)
                except TimeoutException:
                    pass
                else:
                    break
            else:
                continue

            if type(train_info) is TrainInfo:
                trains_info_list.append(train_info)
            else:
                wait_list.append(train_info)

        return TrainsAnswer(trains_list=trains_info_list, wait_list=wait_list)

    def _parse_train(self, train: WebElement) -> ShortTrainInfo:
        parsed_url = urlparse(self.__driver.current_url)
        nnst1 = int(parse_qs(parsed_url.query)['nnst1'][0])
        nnst2 = int(parse_qs(parsed_url.query)['nnst2'][0])

        departure_station = {
            'nnst': nnst1,
            'time': train.find_element(By.XPATH, settings.TUTURU_URL.XPATH.TRAINS_LIST_PAGE.DEPARTURE_TIME).text,
            'date': train.find_element(By.XPATH, settings.TUTURU_URL.XPATH.TRAINS_LIST_PAGE.DEPARTURE_DATE).text,
            'title': train.find_element(By.XPATH, settings.TUTURU_URL.XPATH.TRAINS_LIST_PAGE.DEPARTURE_TITLE).text,
            'city': train.find_element(By.XPATH, settings.TUTURU_URL.XPATH.TRAINS_LIST_PAGE.DEPARTURE_CITY).text,
        }
        arrival_station = {
            'nnst': nnst2,
            'time': train.find_element(By.XPATH, settings.TUTURU_URL.XPATH.TRAINS_LIST_PAGE.ARRIVAL_TIME).text,
            'date': train.find_element(By.XPATH, settings.TUTURU_URL.XPATH.TRAINS_LIST_PAGE.ARRIVAL_DATE).text,
            'title': train.find_element(By.XPATH, settings.TUTURU_URL.XPATH.TRAINS_LIST_PAGE.ARRIVAL_TITLE).text,
            'city': train.find_element(By.XPATH, settings.TUTURU_URL.XPATH.TRAINS_LIST_PAGE.ARRIVAL_CITY).text,
        }
        train_info = {
            'train_number': train.find_element(By.XPATH, settings.TUTURU_URL.XPATH.TRAINS_LIST_PAGE.TRAIN_NUMBER).text,
            'trip_time': train.find_element(By.XPATH, settings.TUTURU_URL.XPATH.TRAINS_LIST_PAGE.TRAIN_TRIP_TIME).text,
            'departure_station': departure_station,
            'arrival_station': arrival_station,
        }
        buy_segments = train.find_elements(By.XPATH, settings.TUTURU_URL.XPATH.TRAINS_LIST_PAGE.TRAIN_BUY_SECTION)
        if len(buy_segments) > 2:
            return ShortTrainInfo(**train_info)

        choose_seats_button = train.find_element(
            By.XPATH, settings.TUTURU_URL.XPATH.TRAINS_LIST_PAGE.CHOOSE_SEATS_BUTTON)
        self.__driver.execute_script(
            "arguments[0].click();", choose_seats_button)

        original_window = self.__driver.current_window_handle
        for window_handle in self.__driver.window_handles:
            if window_handle != original_window:
                self.__driver.switch_to.window(window_handle)
                break

        WebDriverWait(self.__driver, settings.SELENIUM_CONF.PAGE_LOAD_DELAY).until(
            EC.presence_of_element_located(
                (By.XPATH, settings.TUTURU_URL.XPATH.TRAIN_PAGE.HEADER))
        )
        train_page_url = self.__driver.current_url
        self._close_tab()
        self.__driver.switch_to.window(original_window)

        return TrainInfo(
            **train_info,
            train_page_url=AnyUrl(train_page_url),
        )
