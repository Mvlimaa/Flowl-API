from fastapi import FastAPI
from app.database import engine, Base
from app.routers import mesas, garcons, produtos, pedidos

app = FastAPI(title="Flowl PDV API")

# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Registra as rotas da API
app.include_router(mesas.router, prefix="/mesas", tags=["Mesas"])
app.include_router(garcons.router, prefix="/garcons", tags=["Garçons"])
app.include_router(produtos.router, prefix="/produtos", tags=["Produtos"])
app.include_router(pedidos.router, prefix="/pedidos", tags=["Pedidos"])