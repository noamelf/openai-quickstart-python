from pydantic import BaseSettings


class Settings(BaseSettings):
    OPENAI_API_KEY: str = "OPENAI_API_KEY"

    class Config:
        env_file = ".env"


settings = Settings()
