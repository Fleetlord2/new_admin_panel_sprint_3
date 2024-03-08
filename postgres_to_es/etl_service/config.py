import backoff
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_OPTIONS: str
    ELASTIC_HOST: str
    ELASTIC_PORT: str
    REDIS_HOST: str
    REDIS_PORT: str

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


settings = Settings()

BACKOFF_CFG = {
    "wait_gen": backoff.expo,
    "exception": Exception,
    "max_tries": 30,
}

POSTGRES_DSN = {
    'dbname': settings.DB_NAME,
    'user': settings.DB_USER,
    'password': settings.DB_PASSWORD,
    'host': settings.DB_HOST,
    'port': settings.DB_PORT,
    'options': settings.DB_OPTIONS,
}

REDIS_DSN = {
    'host': settings.REDIS_HOST,
    'port': settings.REDIS_PORT,
}

ELASTIC_PATH = f"http://{settings.ELASTIC_HOST}:{settings.ELASTIC_PORT}"

FILE = "./state.json"

INDEXES = ['genres', 'movies']

ITERSIZE = 200

TIME_SLEEP = 30
