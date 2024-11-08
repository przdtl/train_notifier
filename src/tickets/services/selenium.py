from pydantic import HttpUrl, BaseModel, PositiveInt

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

from config import settings
from common.exceptions import NoTicketsTrain
from common.services.selenium import TutuParser


class Ticket(BaseModel):
    position: str
    number: PositiveInt


class Carriage(BaseModel):
    number: str
    category: str
    price: str
    tickets: list[Ticket]


class TocketsTutuParser(TutuParser):
    def get_tickets_list(self, url: HttpUrl) -> list[Carriage]:
        self._open_page(url)
        try:
            WebDriverWait(self.__driver, settings.SELENIUM_CONF.PAGE_LOAD_DELAY).until(
                EC.presence_of_element_located(
                    (By.XPATH, settings.TUTURU_URL.XPATH.TRAIN_PAGE.HEADER)
                ))
        except TimeoutException:
            raise NoTicketsTrain

        category_list = self.__driver.find_elements(
            By.XPATH, settings.TUTURU_URL.XPATH.TRAIN_PAGE.CATEGORY_LIST
        )
        carriages = []
        for carriage_category in category_list:
            category_title = carriage_category.find_element(
                By.XPATH, 'span'
            ).text
            carriages_list = carriage_category.find_elements(
                By.XPATH, 'div/div')

            for carriage in carriages_list:
                carriage_number = carriage.find_element(
                    By.XPATH, settings.TUTURU_URL.XPATH.TRAIN_PAGE.CARRIAGE_NUMBER
                ).text
                carriage_prices = carriage.find_elements(
                    By.XPATH, settings.TUTURU_URL.XPATH.TRAIN_PAGE.CARRIAGE_PRICE
                )
                cat_carriage_price = ''.join(
                    [price.text for price in carriage_prices]
                )
                carriages.append(Carriage(
                    price=cat_carriage_price,
                    number=carriage_number,
                    category=category_title,
                    tickets=self._parse_carriage(carriage),
                ))

        return carriages

    def _parse_carriage(self, carriage: WebElement) -> list[Ticket]:
        tickets = []
        show_seats_button = carriage.find_element(
            By.XPATH, settings.TUTURU_URL.XPATH.TRAIN_PAGE.OPEN_CARRIAGE_INFO_BUTTON
        )
        self.__driver.execute_script(
            "arguments[0].click();", show_seats_button)
        seats = carriage.find_elements(
            By.XPATH, settings.TUTURU_URL.XPATH.TRAIN_PAGE.SEAT_ITEM
        )
        for seat in seats:
            ti_type = seat.get_attribute('data-ti-type')
            ti_state = seat.get_attribute('data-ti-state')
            ti_seat = seat.get_attribute('data-ti-seat')

            if not all((ti_type, ti_state, ti_seat)) or ti_state != 'active':
                continue

            tickets.append(Ticket(
                position='верхнее' if ti_type == 'top' else 'нижнее',
                number=int(ti_seat),  # type: ignore
            ))

        return tickets
