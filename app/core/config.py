from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    mongodb_url: str = Field(..., env="MONGODB_URL")
    mongodb_db: str = Field("orderdb", env="MONGODB_DB")
    tax_rates_file: str = Field("app/resources/tax_rates.json", env="TAX_RATES_FILE")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
