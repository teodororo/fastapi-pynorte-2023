from fastapi import FastAPI

from autor_routes import autor_router
from livro_routes import livro_router

app = FastAPI()
app.include_router(autor_router, prefix="/autores",tags=["autor"])
app.include_router(livro_router, prefix="/livros",tags=["livro"])