from pydantic_settings import  BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    app_name: Optional[str] = None
    database_url: Optional[str] = None

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
print(settings)
