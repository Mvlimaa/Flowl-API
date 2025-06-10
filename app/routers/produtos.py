from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Produto)
def criar_produto(produto: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    produto_existente = db.query(models.Produto).filter(
        models.Produto.nome == produto.nome,
        models.Produto.categoria == produto.categoria,
        models.Produto.preco == produto.preco
    ).first()

    if produto_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Produto já existe com os mesmos dados."
        )

    novo_produto = models.Produto(**produto.dict())
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    return novo_produto

@router.get("/", response_model=list[schemas.Produto])
def listar_produtos(db: Session = Depends(get_db)):
    return db.query(models.Produto).all()
