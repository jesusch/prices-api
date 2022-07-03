from pydantic import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY = ""
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    GOOGLEMAPS_API_KEY: str = ''

settings = Settings()