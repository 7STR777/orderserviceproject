from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SECRET_KEY: str = ""
    ALGORITHM: str = ""
    DB_USER: str = ""
    DB_HOST: str = ""
    DB_PORT: int = 5433
    DB_NAME: str = ""
    DB_PASS: str = ""

    @property
    def DATABASE_URL_asyncpg(self):
        return (f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

#.env вида:
# SECRET_KEY = КЛЮЧ
# ALGORITHM = HS256

# DB_NAME=НАЗВАНИЕ
# DB_HOST=localhost
# DB_PORT=5433
# DB_PASS=ПАРОЛЬ
# DB_USER=postgres