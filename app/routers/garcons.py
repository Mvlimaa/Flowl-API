from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db

router = APIRouter()

@router.get("/", response_model=list[dict])
def listar_garcons(db: Session = Depends(get_db)):
    usuarios = db.query(models.Usuario).filter(models.Usuario.categoria == "garcom").all()
    result = []
    for usuario in usuarios:
        garcom = db.query(models.Garcom).filter(models.Garcom.usuario_id == usuario.id).first()
        if garcom:
            id_garcom = garcom.id
        else:
            novo_garcom = models.Garcom(usuario_id=usuario.id)
            db.add(novo_garcom)
            db.commit()
            db.refresh(novo_garcom)
            id_garcom = novo_garcom.id
        result.append({
            "id_garcom": id_garcom,
            "id_usuario": usuario.id,
            "nome_usuario": usuario.nome
        })
    return result

