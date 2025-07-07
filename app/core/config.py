from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mongo_uri: str
    env: str = "local"

    class Config:
        env_file = ".env-dev"

settings = Settings()