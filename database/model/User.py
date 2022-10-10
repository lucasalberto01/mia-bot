from sqlalchemy import Column, Integer, String
from database.engine import Base


class User(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    nome = Column(String(32), unique=True)
    user = Column(String(32))
    humor = Column(String(32))
    pontos = Column(Integer)

    def __repr__(self):
        return f'User {self.username}'

    def __init__(self, id, nome, user, humor, pontos):
        self.id = id
        self.nome = nome
        self.user = user
        self.humor = humor
        self.pontos = pontos
