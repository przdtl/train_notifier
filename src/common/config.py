from pydantic_settings import BaseSettings, SettingsConfigDict


class TelegramWebhookConf(BaseSettings):
    WEB_SERVER_HOST: str = '127.0.0.1'
    WEB_SERVER_PORT: int = 8080

    WEBHOOK_PATH: str = "/webhook"
    BASE_WEBHOOK_URL: str

    model_config = SettingsConfigDict(
        env_prefix='TRAIN_NOTIFIER__TELEGRAM_CONF__WEBHOOK__'
    )


class TelegramConf(BaseSettings):
    TOKEN: str

    WEBHOOK_CONF: TelegramWebhookConf = TelegramWebhookConf()  # type: ignore

    model_config = SettingsConfigDict(
        env_prefix='TRAIN_NOTIFIER__TELEGRAM_CONF__'
    )


class DatabaseConf(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str = 'train_notifier'

    @property
    def CONNECTION_URL(self):
        return "postgresql+asyncpg://{username}:{password}@{host}:{port}/{db_name}".format(
            username=self.DB_USER,
            password=self.DB_PASS,
            host=self.DB_HOST,
            port=self.DB_PORT,
            db_name=self.DB_NAME,
        )

    model_config = SettingsConfigDict(
        env_prefix='TRAIN_NOTIFIER__DB_CONF__'
    )


class TaskiqConf(BaseSettings):
    BROKER_URL: str
    BACKEND_URL: str

    model_config = SettingsConfigDict(
        env_prefix='TRAIN_NOTIFIER__TASKIQ_CONF__'
    )


class Settings(BaseSettings):
    # Telegram bot conf
    TELEGRAM_CONF: TelegramConf = TelegramConf()  # type: ignore

    # Celery conf
    TASKIQ_CONF: TaskiqConf = TaskiqConf()  # type: ignore

    # Mongodb conf
    DB_CONF: DatabaseConf = DatabaseConf()  # type: ignore

    model_config = SettingsConfigDict(
        env_prefix='TRAIN_NOTIFIER__',
    )


settings = Settings()
