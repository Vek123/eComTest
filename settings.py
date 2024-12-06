from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Example API"
    app_host: str = "0.0.0.0"
    app_port: int = 8000

    project_root: Path = Path(__file__).parent.resolve()

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
