#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String
from src.database.connect import Base


class History(Base):
    """Classe que representa a tabela historico de pontos"""
    __tablename__ = 'historico'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    frase = Column(String(50))
    humor = Column(String(50))
    pontos = Column(String(50))
    tempo = Column(String(50))

    def __repr__(self):
        return '<History %r>' % (self.nome)

    def __init__(self, user_id, frase, humor, pontos, tempo):
        self.user_id = user_id
        self.frase = frase
        self.humor = humor
        self.pontos = pontos
        self.tempo = tempo
