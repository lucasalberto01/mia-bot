import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

engine = create_engine(os.getenv("DB_URL"), echo=True, future=True)
session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = session.query_property()


def init_db():
    from .model.Conversation import Conversation
    from .model.User import User
    from .model.UserActive import UserActive
    from .model.History import History
    from .model.UserGroup import UserGroup

    Base.metadata.create_all(bind=engine)


init_db()
