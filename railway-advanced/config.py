import os

class Config:
    MYSQL_HOST = "localhost"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_DATABASE = "railwaydb"
    MYSQL_PORT = 3306
    SECRET_KEY = "railway-advanced-secret"