from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Produto)
def criar_produto(produto: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    try:
        categoria_enum = models.CategoriaEnum(produto.categoria)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Categoria inválida."
        )

    produto_existente = db.query(models.Produto).filter(
        models.Produto.nome == produto.nome,
        models.Produto.categoria == categoria_enum,
        models.Produto.preco == produto.preco
    ).first()

    if produto_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Produto já existe com os mesmos dados."
        )

    novo_produto = models.Produto(
        nome=produto.nome,
        preco=produto.preco,
        categoria=categoria_enum
    )
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    return novo_produto

@router.get("/", response_model=list[schemas.Produto])
def listar_produtos(db: Session = Depends(get_db)):
    return db.query(models.Produto).all()

@router.delete("/{produto_id}", status_code=204)
def deletar_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(models.Produto).filter(models.Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    db.query(models.ItemPedido).filter(models.ItemPedido.produto_id == produto_id).delete()
    db.delete(produto)
    db.commit()
    return None