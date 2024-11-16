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


class MongoDBConf(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str = 'train_notifier'

    model_config = SettingsConfigDict(
        env_prefix='TRAIN_NOTIFIER__MONGODB_CONF__'
    )


class CeleryConf(BaseSettings):
    BROKER_URL: str
    BACKEND_URL: str

    model_config = SettingsConfigDict(
        env_prefix='TRAIN_NOTIFIER__CELERY_CONF__'
    )


class Settings(BaseSettings):
    # Telegram bot conf
    TELEGRAM_CONF: TelegramConf = TelegramConf()  # type: ignore

    # Celery conf
    CELERY_CONF: CeleryConf = CeleryConf()  # type: ignore

    # Mongodb conf
    MONGODB_CONF: MongoDBConf = MongoDBConf()  # type: ignore

    model_config = SettingsConfigDict(
        env_file='.env',
        env_prefix='TRAIN_NOTIFIER__',
        # arbitrary_types_allowed=True
    )


settings = Settings()
