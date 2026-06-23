import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "local"
    app_port: int = 8000

    aws_access_key_id: str
    aws_secret_access_key: str
    aws_default_region: str = "us-east-1"
    aws_s3_bucket: str

    model_config = SettingsConfigDict(
        env_file = os.path.join(os.path.dirname(__file__), "../.env"),
        env_file_encoding= "utf-8",
        extra="ignore"
    )

settings = Settings()

