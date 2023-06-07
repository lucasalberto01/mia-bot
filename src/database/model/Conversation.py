from sqlalchemy import Column, Integer, String
from src.database.connect import Base


class Conversation(Base):
    __tablename__ = 'conversa'
    id = Column(Integer, primary_key=True)
    nome = Column(String(50))
    user = Column(String(50))
    fala = Column(String(50))
    tempo = Column(String(50))

    def __init__(self, id, nome, user, fala, tempo):
        self.id = id
        self.nome = nome
        self.user = user
        self.fala = fala
        self.tempo = tempo

    def __repr__(self):
        return '<Conversa %r>' % (self.nome)
