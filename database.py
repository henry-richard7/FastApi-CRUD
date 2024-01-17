from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from configparser import ConfigParser

config = ConfigParser()
config.read("config.conf")

username = config["MYSQL"]["username"]
password = config["MYSQL"]["password"]
address = config["MYSQL"]["ip"]
port = config["MYSQL"]["port"]
database = config["MYSQL"]["database"]

URL_DATABASE = f"mysql+pymysql://{username}:{password}@{address}/{database}"

engine = create_engine(URL_DATABASE, pool_size=10, max_overflow=30)
Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
