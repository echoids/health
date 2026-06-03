from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # 数据库
    database_url: str = "mysql+pymysql://root:root@localhost:3306/meishi?charset=utf8mb4"
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    # JWT
    jwt_secret: str = "dev-secret-change-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_days: int = 7
    refresh_token_expire_days: int = 30
    # 微信
    wechat_appid: str = ""
    wechat_secret: str = ""


settings = Settings()
