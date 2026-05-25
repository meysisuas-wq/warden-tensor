from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    APP_NAME: str = "WardenTensor"
    APP_ENV: str = Field(default="development")
    APP_DEBUG: bool = Field(default=True)
    APP_PORT: int = Field(default=8002)
    APP_SECRET_KEY: str = Field(default="change-me")
    DATABASE_URL: str = Field(default="postgresql+asyncpg://warden:password@localhost:5432/wardentensor")
    DATABASE_POOL_SIZE: int = Field(default=25)
    REDIS_URL: str = Field(default="redis://localhost:6379/2")
    ROCM_ENABLED: bool = Field(default=False)
    ROCM_DEVICE_ID: int = Field(default=0)
    INFERENCE_BATCH_SIZE: int = Field(default=8)
    MAX_STREAMS: int = Field(default=100)
    STREAM_BUFFER_SIZE: int = Field(default=30)
    FRAME_SKIP: int = Field(default=2)
    CONFIDENCE_THRESHOLD: float = Field(default=0.65)
    NMS_THRESHOLD: float = Field(default=0.45)
    ALERT_COOLDOWN_SECONDS: int = Field(default=30)
    MAX_ALERTS_PER_MINUTE: int = Field(default=100)
    LOG_LEVEL: str = Field(default="INFO")
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
