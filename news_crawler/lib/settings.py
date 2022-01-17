from pydantic import BaseSettings


class Settings(BaseSettings):
    twitter_consumer_key: str
    twitter_consumer_secret: str
    twitter_token: str
    twitter_token_secret: str

    class Config:
        env_file = ".env"


settings = Settings()
