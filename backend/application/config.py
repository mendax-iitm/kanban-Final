import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL="redis://localhost:6379/1"
    CELERY_RESULT_BACKEND="redis://localhost:6379/2"
    SMTP_SERVER_HOST= "localhost"
    SMTP_SERVER__PORT= 1025
    SENDER_ADDRESS= "email@abhishek.com"
    SENDER_PASSWORD= ""
    REDIS_URL="redis://localhost:6379"
    CACHE_TYPE="RedisCache"
    CACHE_REDIS_HOST="localhost"
    CACHE_REDIS_PORT=6379
    CACHE_DEFAULT_TIMEOUT=300
    

class LocalDevelopmentConfig(Config):
    SQLITE_DB_DIR = os.path.join(basedir, "../db_directory")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
        SQLITE_DB_DIR, "testdb.sqlite3"
    )
    
    DEBUG = False
    SECRET_KEY = "23y9afguygf7geyfg"
    SECURITY_PASSWORD_HASH = "bcrypt"
    SECURITY_PASSWORD_SALT = "really super secret"
    JWT_SECRET_KEY = "21f1002429" 
    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_UNAUTHORIZED_VIEW = None
    REDIS_URL = "redis://localhost:6379"
    CELERY_BROKER_URL="redis://localhost:6379/1"
    CELERY_RESULT_BACKEND="redis://localhost:6379/2"
    SMTP_SERVER_HOST= "localhost"
    SMTP_SERVER__PORT= 1025
    SENDER_ADDRESS= "email@abhishek.com"
    SENDER_PASSWORD= ""
    REDIS_URL="redis://localhost:6379"
    REDIS_URL="redis://localhost:6379"
    CACHE_TYPE="RedisCache"
    CACHE_REDIS_HOST="localhost"
    CACHE_REDIS_PORT=6379
    CACHE_DEFAULT_TIMEOUT=300

    