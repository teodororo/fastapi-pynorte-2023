**Opção 1**
```Python
minha_lista = [
    1, 2, 3,
    4, 5, 6,
    ]
resultado = minha_funcao_que_aceita_varios_parametros(
    'a', 'b', 'c',
    'd', 'e', 'f',
    )
```

**Opção 2**
```Python
minha_lista = [
    1, 2, 3,
    4, 5, 6,
]
resultado = minha_funcao_que_aceita_varios_parametros(
    'a', 'b', 'c',
    'd', 'e', 'f',
)
```

# FastAPI de cabo a rabo
Código e slides do workshop apresentado na Python Norte 2023.

## Instalação
Python 3.7+

```console
pip3 install "fastapi[all]"
```

```console
pip3 install pytest-cov
```
```console
pip3 install sqlalchemy
```
## Agenda
- [Hello, world!](#hello-world)
	- [Teste automático](#teste-automático)
 	- [Marcando rotas descontinuadas](#marcando-rotas-descontinuadas)
	- [Dividindo as rotas com _tags_](#dividindo-as-rotas-com-tags)
- [CRUD](#crud)
  	- [Esqueleto do schema](#esqueleto-do-schema)
  	- [Esqueleto dos models](#esqueleto-dos-models)
  	- [CRUD real oficial](#crud-real-oficial)
  	 	- [Injeção de dependência](#injeção-de-dependência)
  		- [Parâmetros do path](#parâmetros-do-path)
  	   	- [Parse de schema para model](#parse-de-schema-para-model)
  	   	- []
- [Troubleshooting](#troubleshooting)


## Hello, world!
```Python
# main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def main():
	return {"hello":"world"}
```
Para executar, assumindo que o arquivo se chama "main.py":
```console
python3 -m uvicorn main:app --reload
```
Caso queira rodar em segundo plano, adicione "&" no final do comando. Há outras opções de parâmetros, por exemplo:
```console
python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 88 --workers 4 ... &
```
Saiba mais na [documentação oficial do Uvicorn](https://www.uvicorn.org/).

Para visualizar o Swagger, acesse:
```
http://0.0.0.0:8000/docs
```
Para visualizar o ReDoc, acesse:
```
http://0.0.0.0:8000/redoc
```
Para visualizar o .json do OpenAPI, acesse:
```
http://0.0.0.0:8000/openapi.json
```
Tudo isso foi gerado automaticamente.
### Teste automático
Continuando, se rodarmos:

```console
pytest --cov=. --cov-report=html
```
E abrimos o diretório "htmlcov", o arquivo "main_py.html" irá nos informar que nada foi testado.

Então, crie um arquivo chamado "test_get.py" e copie o seguinte _script_:
```Python
# test_get.py
from fastapi.testclient import TestClient
from main import app

def test_hello_world():
	client = TestClient(app)
	response = client.get('/')
	assert response.status_code == 200
	assert response.json() == {'hello': 'world'}
```
Agora, ao rodar o comando:
```console
pytest --cov=. --cov-report=html
```
O "main_py.html" estará todo verde. Eba.
### Marcando rotas descontinuadas
É possível marcar uma rota como descontinuada.
```Python
# main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/", deprecated=True)
def main():
	return {"hello":"world"}
```
### Dividindo as rotas com _tags_
É possível dividir as rotas com uso das _tags_. O FastAPI recomenda que seja criado um Enum para melhorar o gerenciamento.

Lembrando, a ordem de escrita das rotas importa.
```Python
# main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/root",tags=["root"])
def main():
	return {"hello":"world"}

@app.get("/", deprecated=True, tags=["descontinuada"])
def main():
	return {"hello":"world"}
```
## CRUD
Vamos fazer o sistema de uma biblioteca com as seguintes tabelas:
```SQL
CREATE TABLE autores (
        cpf VARCHAR NOT NULL, 
        nome VARCHAR, 
        PRIMARY KEY (cpf)
)
```

```SQL
CREATE TABLE livros (
        isbn VARCHAR NOT NULL, 
        titulo VARCHAR, 
        PRIMARY KEY (isbn)
)
```
```SQL
CREATE TABLE livro_autor (
        livro_isbn VARCHAR NOT NULL, 
        autor_cpf VARCHAR NOT NULL, 
        PRIMARY KEY (livro_isbn, autor_cpf), 
        FOREIGN KEY(livro_isbn) REFERENCES livros (isbn), 
        FOREIGN KEY(autor_cpf) REFERENCES autores (cpf)
)
```
A chave primária da tabela livro_autor é uma chave conjunta das duas chaves estrangeiras. Essa tabela só existe porque é uma relação N-N.
### Esqueleto do schema
O que é um livro?

Um livro é um objeto.

Um objeto, para ser instancidado, precisa de uma classe. 
```Python
class Livro:
    def __init__(self, isbn, titulo): # construtor
        self.isbn= isbn
        self.titulo= titulo
```
Agora, vamos instanciá-lo:
```Python
livros = [Livro(isbn="123", titulo="Vidas Secas")]
```
Poxa, conforme escrevemos os atributos, a IDE não nos diz qual o tipo dos atributos...

Então, vamos substituí-lo por um BaseModel do pydantic na classe:
```Python
from pydantic import BaseModel
class Livro(BaseModel):
	isbn: str
	titulo: str
```

Podia ser um @dataclass também, assim:

```Python
from dataclassesimport dataclass
class Livro(BaseModel):
	isbn: str
	titulo: str
```
Mas como o FastAPI diz que o pydantic é legal, vamos usar o pydantic.

E já que criamos o schema, vamos usá-lo para servir de exemplo no Swagger.

No final, nosso código inteiro estará assim:
```Python
# main.py
from fastapi import FastAPI

from pydantic import BaseModel

from typing import List

app = FastAPI()


class Livro(BaseModel):
    isbn: str
    titulo: str


@app.get("/livros", tags=["Livros"], response_model=List[Livro])
def main():
    livros = [Livro(isbn="123", titulo="Vidas Secas"),
              Livro(isbn="321", titulo="Os Sertoes")]
    return livros
```
Vamos criar um arquivo chamado **schemas.py** para guardar os schemas?
```Python
# schemas.py
from pydantic import BaseModel

class AutorSchema(BaseModel):
    cpf: str
    nome: str

class LivroSchema(BaseModel):
    isbn: str
    titulo: str
```
Assim, o **main.py** fica mais enxuto:
```Python
# main.py
from typing import List

from fastapi import FastAPI

import schemas

app = FastAPI()


@app.get("/livros", tags=["Livros"], response_model=List[schemas.Livro])
def main():
    livros = [schemas.Livro(isbn="123", titulo="Vidas Secas"),
              schemas.Livro(isbn="321", titulo="Os Sertoes")]
    return livros
```
### Esqueleto dos models
Vamos falar sobre o elefante branco na sala. Vamos falar do SGBD.

Bom, antes de fazer esse tutorial, eu nunca tinha usado o SQLAlchemy. Fiz um experimento sem relação com o FastAPI e ele está nesse repositório dentro de utils/database.py

Enfim, como não é o objetivo do tutorial, vamos apenas copiar e colar os trechos de código abaixo e salvá-los na raiz:

```Python
# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///data.db', echo=True)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()
```

```Python
# models.py
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
```
Easy.
Aqui como vai ficar o **main.py**:
```Python
# main.py
from typing import List
from fastapi import FastAPI

import schemas
import models

from sqlalchemy.orm import Session
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

def get_db():  # dependencia
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()


@app.get("/livros", tags=["Livros"], response_model=List[schemas.Livro])
def main():
    livros = [schemas.Livro(isbn="123", titulo="Vidas Secas"),
              schemas.Livro(isbn="321", titulo="Os Sertoes")]
    return livros
```
### CRUD real oficial
Agora vamos escrever as rotas que faltam e conectá-las à base de dados.
#### Injeção de dependência
É preciso que a base de dados exista antes que você faça um CRUD nela. No entanto, se adicionarmos algo como:
```Python
@app.get("/livros", tags=["Livros"], response_model=List[schemas.Livro])
def main(db: Session = get_db()):
    livros = db.query(models.Livro).all()
    return livros
```
Vai dar erro porque ele está esperando um objeto, não uma função. Vamos, então, usar o _Depends_ do FastAPI. Nosso **main.py** vai ficar assim, ó:
```Python
from typing import List
from fastapi import FastAPI, Depends

import schemas
import models

from sqlalchemy.orm import Session
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

def get_db():  # dependencia
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()


@app.get("/livros", tags=["Livros"], response_model=List[schemas.Livro])
def main(db: Session = Depends(get_db)):
    livros = db.query(models.Livro).all()
    return livros
```
E, se testarmos, vai retornar [] porque não tem nada lá. Ainda não fizemos o post.

Enfim, vamos cuidar disso depois. O que importa Depends() é forte. É com ele que conseguimos, por exemplo, fazer a validação do CPF (também é preciso ter fé).

#### Parâmetros do path
Antes do post, vamos aproveitar que ainda estamos no get e fazer um exemplo de query pelos parâmetros do _path_. Por exemplo, um limite de itens. O front sempre pede isso.
```Python
@app.get("/livros", tags=["Livros"], response_model=List[schemas.Livro])
def get_livros(db: Session = Depends(get_db),limit:int = 10):
    livros = db.query(models.Livro).all()
    return livros[:limit:]
```
Legal. Sabe mais o que dá para fazer? Um Enum. O front sempre pede isso.
```Python
from enum import Enum

class Livros(Enum):
    vidas_secas = 'Vidas Secas'
    os_sertoes = 'Os Sertoes'

@app.get("/livros", tags=["Livros"], response_model=List[schemas.Livro])
def get_livros(livros: Livros,db: Session = Depends(get_db),limit:int = 10):
    livros = db.query(models.Livro).all()
    return livros[:limit:]
```
Ok, chega.
#### Parse de schema para model
Tenho certeza que não vai dar para explicar isso no tutorial. Mas, assim, para instanciar um "Livro" no banco de dados é assim:

## Troubleshooting
Para parar o FastAPI:

```console
fuser -k 8000/tcp
```
