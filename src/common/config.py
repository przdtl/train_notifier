from pydantic import BaseModel

from pydantic_settings import BaseSettings, SettingsConfigDict


class TelegramWebhookConf(BaseSettings):
    WEB_SERVER_HOST: str = "127.0.0.1"
    WEB_SERVER_PORT: int = 8080

    WEBHOOK_PATH: str = "/webhook"
    BASE_WEBHOOK_URL: str

    model_config = SettingsConfigDict(
        env_prefix="TRAIN_NOTIFIER__TELEGRAM_CONF__WEBHOOK__"
    )


class TelegramConf(BaseSettings):
    TOKEN: str

    WEBHOOK_CONF: TelegramWebhookConf = TelegramWebhookConf()  # type: ignore

    model_config = SettingsConfigDict(env_prefix="TRAIN_NOTIFIER__TELEGRAM_CONF__")


class DatabaseConf(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str = "train_notifier"

    @property
    def CONNECTION_URL(self):
        return (
            "postgresql+asyncpg://{username}:{password}@{host}:{port}/{db_name}".format(
                username=self.DB_USER,
                password=self.DB_PASS,
                host=self.DB_HOST,
                port=self.DB_PORT,
                db_name=self.DB_NAME,
            )
        )

    model_config = SettingsConfigDict(env_prefix="TRAIN_NOTIFIER__DB_CONF__")


class TaskiqConf(BaseSettings):
    BROKER_URL: str
    BACKEND_URL: str
    SCHEDULE_SOURCE_URL: str

    SCHEDULER_TASK_MINUTES_INTERVAL: int = 5

    model_config = SettingsConfigDict(env_prefix="TRAIN_NOTIFIER__TASKIQ_CONF__")


class TuTuRoutesXPath(BaseModel):
    DEPARTURE_ST_INPUT: str = (
        '//*[@id="wrapper"]/div[3]/div/form/div/div/div[1]/div/div[1]/div[1]/input'
    )
    ARRIVAL_ST_INPUT: str = (
        '//*[@id="wrapper"]/div[3]/div/form/div/div/div[3]/div/div[1]/div[1]/input'
    )
    DATE_INPUT: str = (
        '//*[@id="wrapper"]/div[3]/div/form/div/div/div[4]/div/div[1]/div/input'
    )

    FIRST_DEPARTURE_CITY_HINTING: str = (
        '//*[@id="wrapper"]/div[3]/div/form/div/div/div[1]/div/div[1]/div[2]/div[1]/ul/li[1]/div'
    )
    FIRST_ARRIVAL_CITY_HINTING: str = (
        '//*[@id="wrapper"]/div[3]/div/form/div/div/div[3]/div/div[1]/div[2]/div[1]/ul/li[1]/div'
    )

    SHOW_SCHEDULE_BUTTON: str = (
        '//*[@id="wrapper"]/div[3]/div/form/div/div/div[6]/button'
    )

    SHOW_ROUTE_BUTTON: str = (
        '//*[@id="wrapper"]/div[3]/div[4]/div/div[4]/div/div/div/div/div[1]/button'
    )


class TuTuTrainsListXPath(BaseModel):
    TRAINS_LIST: str = '//*[@id="root"]/div/div[3]/div/div[3]/div'

    DEPARTURE_TIME: str = "div[1]/div/div/div[1]/div/div[2]/div[1]/div[1]/span[1]"
    DEPARTURE_DATE: str = (
        "div[1]/div/div/div[1]/div/div[2]/div[1]/div[3]/div[1]/span[1]"
    )

    ARRIVAL_TIME: str = "div[1]/div/div/div[1]/div/div[2]/div[1]/div[1]/span[3]"
    ARRIVAL_DATE: str = "div[1]/div/div/div[1]/div/div[2]/div[1]/div[3]/div[2]/span[1]"

    TRAIN_NUMBER: str = "div/div/div/div[1]/div/div[1]/div[1]/div/div[1]/span/span"
    TRAIN_TRIP_TIME: str = "div[1]/div/div/div[1]/div/div[2]/div[1]/div[1]/span[2]"

    CHOOSE_SEATS_BUTTON: str = (
        "div[1]/div/div/div[2]/div/div[2]/div[2]/div[2]/div/button"
    )


class TuTuTrainXPath(BaseModel):
    CARRIAGE_NUMBER: str = "div/div/div/div/div/div/div[1]/div[1]/div/span[1]"
    OPEN_CARRIAGE_INFO_BUTTON: str = (
        "div/div/div/div/div/div/div[1]/div[4]/div/div/div/button"
    )
    CLOSE_CARRIAGE_INFO_BUTTON: str = (
        "div/div/div/div/div/div/div[1]/div[4]/div/div/button"
    )
    SEAT_ITEM: str = "div/div/div/div/div/div/div[2]/div/div[4]/div/div/div/div/div/div"


class TuTuXPath(BaseModel):
    ROUTES_PAGE: TuTuRoutesXPath = TuTuRoutesXPath()
    TRAINS_LIST_PAGE: TuTuTrainsListXPath = TuTuTrainsListXPath()
    TRAIN_PAGE: TuTuTrainXPath = TuTuTrainXPath()


class TutuConf(BaseModel):
    SEARCH_ROUTES_URL: str = "https://www.tutu.ru/poezda"
    TRAINS_LIST_PAGE_BASE_URL: str = "https://www.tutu.ru/poezda/rasp_d.php"

    XPATH: TuTuXPath = TuTuXPath()


class TicketServices(BaseModel):
    TUTU_CONF: TutuConf = TutuConf()


class Settings(BaseSettings):
    # Telegram bot conf
    TELEGRAM_CONF: TelegramConf = TelegramConf()  # type: ignore

    # Taskiq conf
    TASKIQ_CONF: TaskiqConf = TaskiqConf()  # type: ignore

    # DB conf
    DB_CONF: DatabaseConf = DatabaseConf()  # type: ignore

    # Railway ticket services
    TICKET_SERVICES: TicketServices = TicketServices()

    model_config = SettingsConfigDict(
        env_prefix="TRAIN_NOTIFIER__",
    )


settings = Settings()
