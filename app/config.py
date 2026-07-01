from pydantic_settings import BaseSettings

class Settings(BaseSettings):
  CLIENT_URL: str = "http://localhost:5173"

  class Config:
    env_file = ".env"

settings = Settings()