from pydantic import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY = ""
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    GOOGLEMAPS_API_KEY: str = ''
    BUCKET = 'alcolina-pbras-prices'


    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

settings = Settings()