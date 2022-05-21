"""
Setup Configuration for Application
"""

from pydantic import BaseSettings


class Settings(BaseSettings):
    # Database
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str

    # Authentication
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"


settings = Settings()
