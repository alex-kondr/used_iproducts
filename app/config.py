from datetime import timedelta

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    sqlalchemy_uri: str = "mysql+aiomysql://127.0.0.1:1487/db"
    authjwt_secret_key: str = "your_secret_key"
    algorithm: str = "HS256"
    authjwt_access_token_expires: timedelta = timedelta(minutes=60)
    
settings = Settings()   
# print(settings)