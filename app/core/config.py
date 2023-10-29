from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_NAME: str
    DB_PASS: str
    DATABASE_URL: str
    EXCHANGE_API_KEY: str
    MODE: str

    class Config:
        env_file = ".env"


settings = Settings()
