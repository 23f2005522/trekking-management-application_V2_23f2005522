from datetime import timedelta


class Config:
    SECRET_KEY = "supersecretkey23f2005522" 
    JWT_SECRET_KEY = "jwtsecretkey23f2005522_"   
    SQLALCHEMY_DATABASE_URI = "sqlite:///Trek.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False 
    CACHE_TYPE = "RedisCache"   
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=3)

    # Redis 
    REDIS_URL = "redis://localhost:6379/0"          # SSE + caching
    CELERY_BROKER_URL = "redis://localhost:6379/1"  # Celery broker
    CELERY_RESULT_BACKEND = "redis://localhost:6379/2"  # Celery results

    # MailHog — (local email testing)
    SMTP_HOST = "localhost"
    SMTP_PORT = 1025
    SENDER_EMAIL = "admin@tma.com"
    SENDER_PASSWORD = ""
