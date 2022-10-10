from sqlalchemy import Column, Integer, String
from database.engine import Base


class UserGroup(Base):
    __tablename__ = 'grupo_usuario'
    id_grupo = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, primary_key=True)
    nome_grupo = Column(String(50))
    nome_usuario = Column(String(50))
    user_usuario = Column(String(50))

    def __init__(self, id_grupo, id_usuario, nome_grupo, nome_usuario, user_usuario):
        self.id_grupo = id_grupo
        self.id_usuario = id_usuario
        self.nome_grupo = nome_grupo
        self.nome_usuario = nome_usuario
        self.user_usuario = user_usuario

    def __repr__(self):
        return '<UserGroup %r>' % (self.nome_usuario)
