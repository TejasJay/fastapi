from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Tell pydantic-settings to load from .env
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # This is REQUIRED, and must exist in env or .env
    DATABASE_URL: str

settings = Settings()
