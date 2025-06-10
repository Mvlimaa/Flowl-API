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
