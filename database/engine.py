from sqlalchemy.ext.declarative import declarative_base
from .connect import engine, session

Base = declarative_base()
session = session
