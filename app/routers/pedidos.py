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
