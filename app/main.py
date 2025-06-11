from fastapi import FastAPI
from app.database import engine, Base
from app.routers import mesas, garcons, produtos, pedidos
from fastapi.middleware.cors import CORSMiddleware
from app.routers import usuarios

app = FastAPI(title="Flowl PDV API")

# Cria as tabelas no banco de dados.
Base.metadata.create_all(bind=engine)

# Autoriza o Front fazer chamadas.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8081"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registra as rotas da API.
app.include_router(usuarios.router, prefix="/usuarios", tags=["Usuários"])
app.include_router(mesas.router, prefix="/mesas", tags=["Mesas"])
app.include_router(garcons.router, prefix="/garcons", tags=["Garçons"])
app.include_router(produtos.router, prefix="/produtos", tags=["Produtos"])
app.include_router(pedidos.router, prefix="/pedidos", tags=["Pedidos"])
