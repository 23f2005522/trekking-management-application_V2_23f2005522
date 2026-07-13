from datetime import timedelta


class Config:
    SECRET_KEY = "supersecretkey23f2005522" 
    JWT_SECRET_KEY = "jwtsecretkey23f2005522_"   
    SQLALCHEMY_DATABASE_URI = "sqlite:///Trek.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=3)

    # celery and redis and SSE
    REDIS_URL = "redis://localhost:6379/0"          # SSE 
    CELERY_BROKER_URL = "redis://localhost:6379/1"  # Celery broker
    CELERY_RESULT_BACKEND = "redis://localhost:6379/2"  # Celery results

    # MailHog — (local email testing)
    SMTP_HOST = "localhost"
    SMTP_PORT = 1025
    SENDER_EMAIL = "mail@TMA.com"
    SENDER_PASSWORD = ""
    # Cashing
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_URL = "redis://localhost:6379/0"
    CACHE_DEFAULT_TIMEOUT = 300

    
    # Redis key prefix name for cached GET /trekker/treks (listing + clear on refresh)
    TREKKER_OPEN_TREKS_KEY = "trekker_open_treks"
