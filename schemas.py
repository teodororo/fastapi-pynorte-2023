from pydantic import BaseModel

class AutorSchema(BaseModel):
    cpf: str
    nome: str

class LivroSchema(BaseModel):
    isbn: str
    titulo: str

class AutorLivroSchema(BaseModel):
    cpf_autor: str
    isbn_livro: str