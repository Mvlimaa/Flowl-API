from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Garcom)
def criar_garcom(garcom: schemas.GarcomCreate, db: Session = Depends(get_db)):
    db_garcom = models.Garcom(nome=garcom.nome)
    db.add(db_garcom)
    db.commit()
    db.refresh(db_garcom)
    return db_garcom

@router.get("/", response_model=list[schemas.Garcom])
def listar_garcons(db: Session = Depends(get_db)):
    return db.query(models.Garcom).all()

@router.delete("/{garcom_id}", status_code=204)
def deletar_garcom(garcom_id: int, db: Session = Depends(get_db)):
    garcom = db.query(models.Garcom).filter(models.Garcom.id == garcom_id).first()
    if not garcom:
        raise HTTPException(status_code=404, detail="Garçom não encontrado")
    db.delete(garcom)
    db.commit()
    return None