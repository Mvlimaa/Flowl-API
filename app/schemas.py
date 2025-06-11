from pydantic import BaseModel
from typing import List, Optional
from enum import Enum
from datetime import datetime
from decimal import Decimal

# Define os tipos de entrada de dados.

# Login
class UsuarioBase(BaseModel):
    nome: str
    cpf: str
    telefone: str

class UsuarioCreate(UsuarioBase):
    senha: str

class UsuarioLogin(BaseModel):
    cpf: str
    senha: str

class UsuarioOut(UsuarioBase):
    id: int

    class Config:
        orm_mode = True

# Mesas 
class MesaBase(BaseModel):
    numero: int

class MesaCreate(MesaBase):
    status: Optional[str] = "fechada"

class MesaUpdateStatus(BaseModel):
    status: str

class Mesa(MesaBase):
    id: int
    status: str

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
class CategoriaCardapio(str, Enum):
    hamburguer = "hamburguer"
    batata = "batata"
    bebida = "bebida"
    sobremesa = "sobremesa"


class ProdutoBase(BaseModel):
    nome: str
    preco: Decimal
    categoria: CategoriaCardapio

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
