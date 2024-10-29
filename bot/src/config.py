from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    TOKEN: str

    model_config = SettingsConfigDict(
        env_file='../.env',
        env_prefix='TRAIN_BOT_',
    )


settings = Settings() # type: ignore
