import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuración de la aplicación"""

    # Servidor
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Selenium/Scraping
    HEADLESS_MODE: bool = True
    TIMEOUT: int = 30

    # Tor
    USE_TOR: bool = False
    TOR_PORT: int = 9050
    TOR_CONTROL_PORT: int = 9051

    # API
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "DIGEMID Medicine Search API"
    VERSION: str = "1.0.0"

    # CORS
    CORS_ORIGINS: list = ["*"]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
