import os

MYSQL_HOST = os.getenv("MYSQL_HOST") or '127.0.0.1'
MYSQL_USER = os.getenv("MYSQL_USER") or 'root'
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD") or 'root'
MYSQL_PORT = os.getenv("MYSQL_PORT") or '3306'
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE") or 'testdb'

# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1:3306/testdb'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT,
                                                                  MYSQL_DATABASE)

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True

REDIS_HOST = os.getenv("REDIS_HOST") or '127.0.0.1'
REDIS_PORT = os.getenv("REDIS_PORT") or '6379'

DEBUG = True
