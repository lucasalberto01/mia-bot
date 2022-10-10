from sqlalchemy import Column, Integer, String
from database.engine import Base


class UserActive(Base):
    __tablename__ = 'ativos'
    id = Column(Integer, primary_key=True)
    nome = Column(String(50))
    tempo = Column(String(50))

    def __init__(self, id, nome, tempo):
        self.id = id
        self.nome = nome
        self.tempo = tempo

    def __repr__(self):
        return '<UserActive %r>' % (self.nome)
