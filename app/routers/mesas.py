from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Mesa)
def criar_mesa(mesa: schemas.MesaCreate, db: Session = Depends(get_db)):
    db_mesa = models.Mesa(numero=mesa.numero)
    db.add(db_mesa)
    db.commit()
    db.refresh(db_mesa)
    return db_mesa

@router.get("/", response_model=list[schemas.Mesa])
def listar_mesas(db: Session = Depends(get_db)):
    return db.query(models.Mesa).all()

@router.get("/abertas", response_model=list[schemas.Mesa])
def listar_mesas_abertas(db: Session = Depends(get_db)):
    return db.query(models.Mesa).filter(models.Mesa.status == "aberta").all()

@router.put("/{mesa_id}/status", response_model=schemas.Mesa)
def atualizar_status_mesa(mesa_id: int, status: str, db: Session = Depends(get_db)):
    mesa = db.query(models.Mesa).filter(models.Mesa.id == mesa_id).first()
    if not mesa:
        raise HTTPException(status_code=404, detail="Mesa não encontrada")
    mesa.status = status
    db.commit()
    db.refresh(mesa)
    return mesa

@router.delete("/{mesa_id}", status_code=204)
def deletar_mesa(mesa_id: int, db: Session = Depends(get_db)):
    mesa = db.query(models.Mesa).filter(models.Mesa.id == mesa_id).first()
    if not mesa:
        raise HTTPException(status_code=404, detail="Mesa não encontrada")
    pedidos = db.query(models.Pedido).filter(models.Pedido.mesa_id == mesa_id).all()
    for pedido in pedidos:
        db.query(models.ItemPedido).filter(models.ItemPedido.pedido_id == pedido.id).delete()
        db.delete(pedido)
    db.delete(mesa)
    db.commit()
    return None