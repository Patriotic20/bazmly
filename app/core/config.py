from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 5
    max_overflow: int = 10


class GoogleConfig(BaseModel):
    client_id: str
    client_secret: str
    redirect_uri: str


class JWTConfig(BaseModel):
    secret_key: str
    algorithm: str = "HS256"
    expire_minutes: int = 60


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        env_file=".env",
        env_file_encoding="utf-8",
    )

    database: DatabaseConfig
    google: GoogleConfig
    jwt: JWTConfig


settings = Settings()
