from sqlalchemy import Column, Integer, String
from database.engine import Base


class Conversation(Base):
    __tablename__ = 'conversa'
    id = Column(Integer, primary_key=True)
    nome = Column(String(50))
    user = Column(String(50))
    fala = Column(String(50))
    tempo = Column(String(50))
