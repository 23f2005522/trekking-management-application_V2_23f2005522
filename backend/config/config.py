from datetime import timedelta


class Config:
    SECRET_KEY = "supersecretkey23f2005522" 
    JWT_SECRET_KEY = "jwtsecretkey23f2005522_"   
    SQLALCHEMY_DATABASE_URI = "sqlite:///Trek.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False 
    CACHE_TYPE = "RedisCache"   
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=3)
