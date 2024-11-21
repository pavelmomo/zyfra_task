from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "API Zyfra Task"
    VERSION: str = "0.0.1"
    SESSION_TTL: int = 5
    USER_FILENAME: str = "user-credits.json"
    SESSION_FILENAME: str = "active-sessions.json"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    ROOT_PATH: str = "/api"


settings = Settings()
