from pydantic_settings import  BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    app_name: Optional[str] = None
    database_url: Optional[str] = None
    test_database_url: Optional[str] = None
    jwt_algorithm: Optional[str] = None
    at_expire_mins: Optional[int] = None
    rt_expire_days: Optional[int] = None
    secret_key: Optional[str] = None
    service_secret: Optional[str] = None

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
