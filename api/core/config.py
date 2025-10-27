from pydantic_settings import  BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    app_name: str | None
    database_url: str | None

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings() # type: ignore
print(settings)
