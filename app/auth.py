from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.database import get_db

# Chave secreta (ideal armazenar via variável de ambiente)
SECRET_KEY = "secreta-muito-forte"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/usuarios/login")

def verificar_senha(senha: str, hashed: str):
    return pwd_context.verify(senha, hashed)

def gerar_hash_senha(senha: str):
    return pwd_context.hash(senha)

def criar_token_acesso(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verificar_token(token: str, db: Session):
    credenciais_invalidas = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido ou expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        cpf: str = payload.get("sub")
        if cpf is None:
            raise credenciais_invalidas
    except JWTError:
        raise credenciais_invalidas
    usuario = crud.get_usuario_by_cpf(db, cpf=cpf)
    if usuario is None:
        raise credenciais_invalidas
    return usuario

def get_usuario_logado(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    return verificar_token(token, db)
