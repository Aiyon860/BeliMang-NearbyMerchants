import secrets
import os
from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    app_name: str = "BeliMang Application"
    debug: bool = False
    secret_key: str = Field(default_factory=lambda: secrets.token_hex(32))
    database_url: str = os.getenv(
        "DATABASE_URL", "postgresql+asyncpg://postgres:root@localhost/merchants_db"
    )


settings = Settings()
