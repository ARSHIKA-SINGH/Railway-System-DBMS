import os


class Config:
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "railwaydb")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
    SECRET_KEY = os.getenv("SECRET_KEY", "railway-advanced-secret")
