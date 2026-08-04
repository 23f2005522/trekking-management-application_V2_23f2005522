import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def _env_bool(name, default=False):
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey23f2005522")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwtsecretkey23f2005522_")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///Trek.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        hours=int(os.getenv("JWT_ACCESS_TOKEN_HOURS", "3"))
    )

    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    RUN_SEED_ON_STARTUP = _env_bool("RUN_SEED_ON_STARTUP", True)

    # Celery and Redis and SSE
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/1")
    CELERY_RESULT_BACKEND = os.getenv(
        "CELERY_RESULT_BACKEND", "redis://localhost:6379/2"
    )

    # SMTP (MailHog for local dev)
    SMTP_HOST = os.getenv("SMTP_HOST", "localhost")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "1025"))
    SENDER_EMAIL = os.getenv("SENDER_EMAIL", "mail@TMA.com")
    SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "")

    # Caching
    CACHE_TYPE = os.getenv("CACHE_TYPE", "RedisCache")
    CACHE_REDIS_URL = os.getenv("CACHE_REDIS_URL", "redis://localhost:6379/0")
    CACHE_DEFAULT_TIMEOUT = int(os.getenv("CACHE_DEFAULT_TIMEOUT", "300"))

    TREKKER_OPEN_TREKS_KEY = os.getenv("TREKKER_OPEN_TREKS_KEY", "trekker_open_treks")

    # CORS — comma-separated origins, e.g. http://localhost:5173,https://yourdomain.com
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")
