from pydantic import BaseModel
from typing import List, Optional
from enum import Enum
from datetime import datetime
from decimal import Decimal

# Mesas 
class MesaBase(BaseModel):
    numero: int

class MesaCreate(MesaBase):
    pass

class Mesa(MesaBase):
    id: int

    class Config:
        orm_mode = True

# Garçons 
class GarcomBase(BaseModel):
    nome: str

class GarcomCreate(GarcomBase):
    pass

class Garcom(GarcomBase):
    id: int

    class Config:
        orm_mode = True

# Produtos 
class CategoriaEnum(str, Enum):
    hamburguer = "Hamburguer"
    batata = "Batata"
    bebida = "Bebida"
    sobremesa = "Sobremesa"

class ProdutoBase(BaseModel):
    nome: str
    preco: Decimal
    categoria: CategoriaEnum

class ProdutoCreate(ProdutoBase):
    pass

class Produto(ProdutoBase):
    id: int

    class Config:
        orm_mode = True

# Pedidos 

class ItemPedido(BaseModel):
    produto_id: int
    quantidade: int

class PedidoBase(BaseModel):
    mesa_id: int
    garcom_id: int
    status: Optional[str] = "pendente"

class PedidoCreate(PedidoBase):
    itens: List[ItemPedido]

class Pedido(PedidoBase):
    id: int
    data_criacao: datetime
    itens: List[ItemPedido]

    class Config:
        orm_mode = True
