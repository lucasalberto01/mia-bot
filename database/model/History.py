from sqlalchemy import Column, Integer, String
from database.engine import Base


class History(Base):
    __tablename__ = 'historico'
    id = Column(Integer, primary_key=True)
    frase = Column(String(50))
    humor = Column(String(50))
    pontos = Column(String(50))
    tempo = Column(String(50))

    def __repr__(self):
        return '<History %r>' % (self.nome)

    def __init__(self, id, frase, humor, pontos, tempo):
        self.id = id
        self.frase = frase
        self.humor = humor
        self.pontos = pontos
        self.tempo = tempo
