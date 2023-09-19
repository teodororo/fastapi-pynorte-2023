from typing import List

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

livro_router = APIRouter()


def get_db():  # Dependency
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@livro_router.get("/", response_model=List[schemas.LivroSchema])
async def read_livro(db: Session = Depends(get_db)):
    livros = db.query(models.Livro).all()
    if livros is None:
        raise HTTPException(status_code=404, detail="Nenhum livro encontrado")
    return livros


@livro_router.post("/", response_model=schemas.LivroSchema)
async def create_livro(livro: schemas.LivroSchema, db: Session = Depends(get_db)):
    db_livro = models.Livro(**livro.model_dump())
    db.add(db_livro)
    db.commit()
    return db_livro


@livro_router.delete("/{cpf}")
async def delete_livro(cpf: str, db: Session = Depends(get_db)):
    livro = db.query(models.Livro).filter(models.Livro.cpf == cpf).first()
    if livro is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    db.delete(livro)
    db.commit()
    return {"message": "Livro deletado com sucesso"}
