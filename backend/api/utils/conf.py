from typing import Optional
from core.utils.conf import BaseSettings, SingletonSettingsMixin


class ApiSettings(SingletonSettingsMixin, BaseSettings):
    docs_url: Optional[str] = None
    redoc_url: Optional[str] = None
    token_algorithm: str = "HS256"
    token_secret: str
    redis_url: str = "redis:6379"
