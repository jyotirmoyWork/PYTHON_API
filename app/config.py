from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_HOSTNAME: str 
    DATABASE_PORT: str
    DATABASE_PASSWORD: str
    DATABASE_NAME:str
    DATABASE_USERNAME: str
    SECRECT_KEY: str 
    ALGORITHMS: str
    ACCESS_TOKEN_EXPIRE_MINUTE: int

    class Config:
        env_file = ".env"

settings = Settings()