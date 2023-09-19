from typing import List

from fastapi import Depends, APIRouter, HTTPException


import models
import schemas

from sqlalchemy.orm import Session
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

autor_router = APIRouter()


def get_db():  # Dependency
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@autor_router.get("/", response_model=List[schemas.AutorSchema])
async def read_autor(db: Session = Depends(get_db)):
    autores = db.query(models.Autor).all()
    if autores is None:
        raise HTTPException(status_code=404, detail="Nenhum autor encontrado")
    return autores


@autor_router.post("/", response_model=schemas.AutorSchema)
async def create_autor(autor: schemas.AutorSchema, db: Session = Depends(get_db)):
    db_autor = models.Autor(**autor.model_dump())
    db.add(db_autor)
    db.commit()
    return db_autor


@autor_router.delete("/{cpf}")
async def delete_autor(cpf: str, db: Session = Depends(get_db)):
    autor = db.query(models.Autor).filter(models.Autor.cpf == cpf).first()
    if autor is None:
        raise HTTPException(status_code=404, detail="Autor não encontrado")
    db.delete(autor)
    db.commit()
    return {"message": "Autor deletado com sucesso"}
