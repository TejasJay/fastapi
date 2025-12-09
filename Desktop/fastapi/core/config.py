from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Configure Pydantic settings using the new v2 syntax
    # model_config replaces the old Config class
    model_config = SettingsConfigDict(
        env_file=".env",           # Load environment variables from .env file
        env_file_encoding="utf-8", # Specify encoding for .env file
        extra="ignore",            # Ignore extra fields in .env that aren't defined in this class
    )

    # The format is postgresql+ASYNC_DRIVER://user:password@host/dbname
    DATABASE_URL: str = "postgresql+asyncpg://postgresql:postgrespass@localhost:5432/fastapi_ecom"
    # DATABASE_SYNC_URL: str = "postgresql+psycopg2://postgres:root@host.docker.internal:5432/fastapi_ecom"
    SECRET_KEY: str
    ALGORITHM: str
    API_AUTH_KEY: str

# Create settings instance - no need to pass extra="ignore" as parameter
settings = Settings()