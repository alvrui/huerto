from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # Base de datos
    DATABASE_URL: str = Field(
        default="postgresql://huerto_user:huerto_pass@localhost:5432/huerto_db",
        env="DATABASE_URL"
    )

    # API AEMET
    AEMET_API_KEY: str = Field(
        default="",
        env="AEMET_API_KEY"
    )

    class Config:
        env_file = ".env"


settings = Settings()
