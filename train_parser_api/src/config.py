from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file='../.env',
        env_prefix='TRAIN_PARSER_',
    )


settings = Settings()
