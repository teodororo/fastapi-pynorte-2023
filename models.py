from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from database import Base


class Autor(Base):
    __tablename__ = 'autores'
    cpf = Column(String, primary_key=True)
    nome = Column(String)
    livros = relationship('Livro', secondary='livro_autor',
                          back_populates='autores')


class Livro(Base):
    __tablename__ = 'livros'
    isbn = Column(String, primary_key=True)
    titulo = Column(String)
    autores = relationship(
        'Autor', secondary='livro_autor', back_populates='livros')


class LivroAutor(Base):
    __tablename__ = 'livro_autor'
    livro_isbn = Column(String, ForeignKey('livros.isbn'), primary_key=True)
    autor_cpf = Column(String, ForeignKey('autores.cpf'), primary_key=True)
