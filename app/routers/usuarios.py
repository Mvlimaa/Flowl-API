from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db
from fastapi.security import OAuth2PasswordRequestForm
from app.auth import criar_token_acesso, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

@router.post("/", response_model=schemas.UsuarioOut)
def criar_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = crud.criar_usuario(db, usuario)
    return db_usuario

@router.get("/", response_model=list[schemas.UsuarioOut])
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(crud.models.Usuario).all()

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = crud.autenticar_usuario(db, form_data.username, form_data.password)
    if not usuario:
        raise HTTPException(status_code=401, detail="CPF ou senha inválidos")

    access_token = criar_token_acesso(
        data={"sub": usuario.cpf}
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.delete("/{usuario_id}", status_code=204)
def deletar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(crud.models.Usuario).filter(crud.models.Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    db.delete(usuario)
    db.commit()
    return None
