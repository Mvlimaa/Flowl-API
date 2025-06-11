from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Pedido)
def criar_pedido(pedido: schemas.PedidoCreate, db: Session = Depends(get_db)):
    mesa_existe = db.query(crud.models.Mesa).filter(crud.models.Mesa.id == pedido.mesa_id).first()
    if not mesa_existe:
        raise HTTPException(status_code=404, detail="Mesa não encontrada")

    garcom_existe = db.query(crud.models.Garcom).filter(crud.models.Garcom.id == pedido.garcom_id).first()
    if not garcom_existe:
        raise HTTPException(status_code=404, detail="Garçom não encontrado")

    return crud.create_pedido(db, pedido)

@router.get("/mesas-abertas", response_model=list[schemas.Mesa])
def listar_mesas_abertas(db: Session = Depends(get_db)):
    return crud.get_mesas_abertas(db)

@router.get("/", response_model=list[schemas.Pedido])
def listar_pedidos(db: Session = Depends(get_db)):
    return crud.get_pedidos(db)

@router.get("/mesa/{mesa_id}", response_model=list[schemas.Pedido])
def listar_pedidos_por_mesa(mesa_id: int, db: Session = Depends(get_db)):
    return crud.get_pedidos_por_mesa(db, mesa_id)

@router.put("/{pedido_id}/status", response_model=schemas.Pedido)
def atualizar_status_pedido(pedido_id: int, status: str, db: Session = Depends(get_db)):
    pedido = crud.update_status_pedido(db, pedido_id, status)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return pedido

@router.delete("/{pedido_id}", status_code=204)
def deletar_pedido(pedido_id: int, db: Session = Depends(get_db)):
    pedido = db.query(crud.models.Pedido).filter(crud.models.Pedido.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    db.delete(pedido)
    db.commit()
    return None
