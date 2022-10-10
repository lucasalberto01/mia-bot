import os
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
load_dotenv()

engine = create_engine(os.getenv("DB_URL"), echo=True, future=True)
Session = sessionmaker(bind=engine)
session = Session()
