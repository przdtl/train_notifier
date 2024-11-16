from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class TuTuRoutesXPath(BaseModel):
    DEPARTURE_ST_INPUT: str = '//*[@id="wrapper"]/div[3]/div/form/div/div/div[1]/div/div[1]/div[1]/input'
    ARRIVAL_ST_INPUT: str = '//*[@id="wrapper"]/div[3]/div/form/div/div/div[3]/div/div[1]/div[1]/input'
    DATE_INPUT: str = '//*[@id="wrapper"]/div[3]/div/form/div/div/div[4]/div/div[1]/div/input'

    FIRST_DEPARTURE_CITY_HINTING: str = '//*[@id="wrapper"]/div[3]/div/form/div/div/div[1]/div/div[1]/div[2]/div[1]/ul/li[1]/div'
    FIRST_ARRIVAL_CITY_HINTING: str = '//*[@id="wrapper"]/div[3]/div/form/div/div/div[3]/div/div[1]/div[2]/div[1]/ul/li[1]/div'

    SHOW_SCHEDULE_BUTTON: str = '//*[@id="wrapper"]/div[3]/div/form/div/div/div[6]/button'


class TuTuTrainsListXPath(BaseModel):
    HEADER: str = '//*[@id="root"]/div/div[3]/div/div[2]/div[2]/div[3]/span[2]'

    TRAINS_LIST: str = '//*[@id="root"]/div/div[3]/div/div[3]/div'

    DEPARTURE_TIME: str = 'div/div/div[2]/div[1]/div/div[2]/div[1]/div[1]/span[1]'
    DEPARTURE_DATE: str = 'div/div/div[2]/div[1]/div/div[2]/div[1]/div[3]/div[1]/span[1]'
    DEPARTURE_TITLE: str = 'div/div/div[2]/div[1]/div/div[2]/div[1]/div[3]/div[1]/span[2]'
    DEPARTURE_CITY: str = 'div/div/div[2]/div[1]/div/div[2]/div[1]/div[3]/div[1]/span[3]'

    ARRIVAL_TIME: str = 'div/div/div[2]/div[1]/div/div[2]/div[1]/div[1]/span[3]'
    ARRIVAL_DATE: str = 'div/div/div[2]/div[1]/div/div[2]/div[1]/div[3]/div[2]/span[1]'
    ARRIVAL_TITLE: str = 'div/div/div[2]/div[1]/div/div[2]/div[1]/div[3]/div[2]/span[2]'
    ARRIVAL_CITY: str = 'div/div/div[2]/div[1]/div/div[2]/div[1]/div[3]/div[2]/span[3]'

    TRAIN_NUMBER: str = 'div/div/div[2]/div[1]/div/div[1]/div[1]/div/div[1]/span/span'
    TRAIN_TRIP_TIME: str = 'div/div/div[2]/div[1]/div/div[2]/div[1]/div[1]/span[2]'

    CHOOSE_SEATS_BUTTON: str = 'div/div/div[2]/div[2]/div/div[2]/div[2]/div[2]/div/button'

    TRAIN_BUY_SECTION: str = 'div/div/div/div[2]/div/div[2]/div'


class TuTuTrainXPath(BaseModel):
    HEADER: str = '//*[@id="root"]/div/div[4]/h1'

    CATEGORY_LIST: str = '//*[@id="root"]/div/div[4]/div[5]/div'
    CARRIAGE_NUMBER: str = 'div/div/div/div/div/div/div[1]/div[1]/div/div/span[1]'
    OPEN_CARRIAGE_INFO_BUTTON: str = 'div/div/div/div/div/div/div[1]/div[4]/div/div/div/button'
    CLOSE_CARRIAGE_INFO_BUTTON: str = 'div/div/div/div/div/div/div[1]/div[4]/div/div/button'
    SEAT_ITEM: str = 'div/div/div/div/div/div/div[2]/div/div[4]/div/div/div/div/div/div'
    CARRIAGE_PRICE: str = 'div/div/div/div/div/div/div[1]/div[3]/div/span'


class TuTuXPath(BaseModel):
    TRAINS_LIST_PAGE: TuTuTrainsListXPath = TuTuTrainsListXPath()
    ROUTES_PAGE: TuTuRoutesXPath = TuTuRoutesXPath()
    TRAIN_PAGE: TuTuTrainXPath = TuTuTrainXPath()


class TuturuConf(BaseModel):
    SEARCH_ROUTES_URL: str = 'https://www.tutu.ru/poezda/'
    SEARCH_TRAINS_URL: str = 'https://www.tutu.ru/poezda/rasp_d.php?nnst1={nnst1}&nnst2={nnst2}&date={date}'

    XPATH: TuTuXPath = TuTuXPath()


class TelegramConf(BaseSettings):
    TOKEN: str

    WEB_SERVER_HOST: str = '127.0.0.1'
    WEB_SERVER_PORT: int = 8080

    WEBHOOK_PATH: str = "/webhook"
    BASE_WEBHOOK_URL: str

    model_config = SettingsConfigDict(
        env_prefix='TRAIN_PARSER_TELEGRAM_CONF_'
    )


class MongoDBConf(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str = 'stations'
    TRAINS_COLLECTION_NAME: str = 'trains'

    model_config = SettingsConfigDict(
        env_prefix='TRAIN_PARSER_MONGODB_CONF_'
    )


class CeleryConf(BaseSettings):
    BROKER_URL: str
    BACKEND_URL: str

    model_config = SettingsConfigDict(
        env_prefix='TRAIN_PARSER_CELERY_CONF_'
    )


class SeleniumConf(BaseSettings):
    PAGE_LOAD_DELAY: int = 5
    REMOTE_URL: str = ''

    model_config = SettingsConfigDict(
        env_prefix='TRAIN_PARSER_SELENIUM_CONF_'
    )


class Settings(BaseSettings):
    # bot conf
    TELEGRAM_CONF: TelegramConf = TelegramConf()  # type: ignore

    # actual url of parsing site
    TUTURU_URL: TuturuConf = TuturuConf()

    # celery conf
    CELERY_CONF: CeleryConf = CeleryConf()

    # mongodb conf
    MONGODB_CONF: MongoDBConf = MongoDBConf()

    # selenium conf
    SELENIUM_CONF: SeleniumConf = SeleniumConf()

    model_config = SettingsConfigDict(
        env_file='.env',
        env_prefix='TRAIN_PARSER_',
        arbitrary_types_allowed=True
    )


settings = Settings()
