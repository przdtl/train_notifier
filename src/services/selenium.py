import pprint
import datetime

from urllib.parse import urlparse
from urllib.parse import parse_qs

from pydantic import HttpUrl, AnyUrl, BaseModel, PositiveInt

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

from config import settings


class Station(BaseModel):
    title: str
    nnst: PositiveInt
    city: str
    date: str
    time: str


class TrainInfo(BaseModel):
    train_number: str
    train_page_url: HttpUrl
    trip_time: str
    departure_station: Station
    arrival_station: Station


class TutuParser:
    def __init__(self) -> None:
        options = Options()
        options.add_argument('--headless')
        self.__driver = webdriver.Firefox(options=options)

    @property
    def driver(self) -> WebDriver:
        return self.__driver

    def _open_page(self, url: HttpUrl) -> None:
        self.__driver.get(str(url))

    def _close_browser(self) -> None:
        self.__driver.quit()

    def _close_tab(self) -> None:
        self.__driver.close()

    def get_trains_list_by_titles(self,
                                  departure_st: str,
                                  arrival_st: str,
                                  date: datetime.date
                                  ) -> list[TrainInfo]:
        self._open_page(AnyUrl(settings.TUTURU_URL.SEARCH_ROUTES_URL))

        departure_station_input = self.__driver.find_element(
            By.XPATH, settings.TUTURU_URL.XPATH.ROUTES_PAGE.DEPARTURE_ST_INPUT)
        arrival_station_input = self.__driver.find_element(
            By.XPATH, settings.TUTURU_URL.XPATH.ROUTES_PAGE.ARRIVAL_ST_INPUT)
        date_input = self.__driver.find_element(
            By.XPATH, settings.TUTURU_URL.XPATH.ROUTES_PAGE.DATE_INPUT)

        departure_station_input.send_keys(departure_st)
        try:
            departure_hinting_element = WebDriverWait(self.__driver, 2).until(
                EC.presence_of_element_located(
                    (By.XPATH, settings.TUTURU_URL.XPATH.ROUTES_PAGE.FIRST_DEPARTURE_CITY_HINTING))
            )
        except TimeoutException:
            return []

        print(f'{departure_hinting_element.text=}')
        departure_hinting_element.click()

        arrival_station_input.send_keys(arrival_st)
        try:
            arrival_hinting_element = WebDriverWait(self.__driver, 2).until(
                EC.presence_of_element_located(
                    (By.XPATH, settings.TUTURU_URL.XPATH.ROUTES_PAGE.FIRST_ARRIVAL_CITY_HINTING))
            )
        except TimeoutException:
            return []
        print(f'{arrival_hinting_element.text=}')
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
                                ) -> list[TrainInfo]:
        url = AnyUrl(settings.TUTURU_URL.SEARCH_TRAINS_URL.format(
            nnst1=nnst1, nnst2=nnst2, date=date.strftime('%d.%m.%Y')
        ))
        self._open_page(url)

        return self._parse_trains_list()

    def _parse_trains_list(self) -> list[TrainInfo]:
        try:
            WebDriverWait(self.__driver, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, settings.TUTURU_URL.XPATH.TRAINS_LIST_PAGE.HEADER))
            )
        except TimeoutException:
            return []

        trains_info_list: list[TrainInfo] = []
        trains_list = self.__driver.find_elements(
            By.XPATH, settings.TUTURU_URL.XPATH.TRAINS_LIST_PAGE.TRAINS_LIST)
        for train in trains_list:
            try:
                train_info = self._parse_train(train)
            except TimeoutException:
                continue

            trains_info_list.append(train_info)

        self._close_browser()

        return trains_info_list

    def get_tickets_list(self, url: HttpUrl) -> list:
        pass

    def _parse_train(self, train: WebElement) -> TrainInfo:
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
        choose_seats_button = train.find_element(
            By.XPATH, settings.TUTURU_URL.XPATH.TRAINS_LIST_PAGE.CHOOSE_SEATS_BUTTON)
        self.__driver.execute_script(
            "arguments[0].click();", choose_seats_button)

        original_window = self.__driver.current_window_handle
        for window_handle in self.__driver.window_handles:
            if window_handle != original_window:
                self.__driver.switch_to.window(window_handle)
                break

        WebDriverWait(self.__driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, settings.TUTURU_URL.XPATH.TRAIN_PAGE.HEADER))
        )
        train_page_url = self.__driver.current_url
        print(train_page_url)
        self._close_tab()
        self.__driver.switch_to.window(original_window)

        return TrainInfo(
            **train_info,
            train_page_url=AnyUrl(train_page_url),
        )

    def _parse_carriage(self) -> None:
        pass

    def _parse_specific_carriage_class(self) -> None:
        pass
