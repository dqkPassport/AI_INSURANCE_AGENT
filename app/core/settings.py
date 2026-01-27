from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Insurance Agent"
    env: str = "dev"

    database_url: str = "sqlite:///./app.db"

    openai_api_key: str | None = None
    openai_model: str = "gpt-5.2"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    jwt_secret: str = "change-me"
    jwt_alg: str = "HS256"
    access_token_expire_minutes: int = 60


settings = Settings()
