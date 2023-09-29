# SCRIPT JUST IN CASE I FORGOT SOMETHING - ITS NOT SUPOSSED TO BE USED
from sqlalchemy import create_engine, Column, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///data.db', echo=True)
Base = declarative_base()

# TABLES
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


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


# INSERT
autor1 = Autor(cpf='12345678901', nome='Autor 1')
autor2 = Autor(cpf='23456789012', nome='Autor 2')

livro1 = Livro(isbn='978-1234567890', titulo='Livro 1')
livro2 = Livro(isbn='978-2345678901', titulo='Livro 2')

publicacao1 = LivroAutor(livro_isbn=livro1.isbn, autor_cpf=autor1.cpf)
publicacao2 = LivroAutor(livro_isbn=livro1.isbn, autor_cpf=autor2.cpf)

session.add_all([autor1, autor2, livro1, livro2, publicacao1, publicacao2])
session.commit()

# SELECT
autores = session.query(Autor).all()
for autor in autores:
    print(autor.nome)  # todos os autores

livros = session.query(Livro).all()
for livro in livros:
    print(livro.titulo)  # todos os livros

publicacoes = session.query(LivroAutor).all()
for publicacao in publicacoes:
    print(publicacao.autor_cpf)  # todos os LivroAutor

autores = session.query(Autor).all()
for autor in autores:
    for livro in autor.livros:
        print(livro.titulo)  # todos os livros de um autor omg funciona msm
