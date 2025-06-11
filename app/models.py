from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime, func, Numeric
from sqlalchemy.orm import relationship
from app.database import Base
import enum

# Criação Data Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cpf = Column(String, unique=True, nullable=False)
    senha = Column(String, nullable=False)
    telefone = Column(String)

class Mesa(Base):
    __tablename__ = "mesas"
    id = Column(Integer, primary_key=True, index=True)
    numero = Column(Integer, unique=True, nullable=False)
    status = Column(String, default="fechada", nullable=False)

    pedidos = relationship("Pedido", back_populates="mesa")


class Garcom(Base):
    __tablename__ = "garcons"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)

    pedidos = relationship("Pedido", back_populates="garcom")

class CategoriaEnum(str, enum.Enum):
    hamburguer = "hamburguer"
    batata = "batata"
    bebida = "bebida"
    sobremesa = "sobremesa"

class Produto(Base):
    __tablename__ = "produtos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    preco = Column(Numeric(10, 2), nullable=False)
    categoria = Column(Enum(CategoriaEnum), nullable=False)

    itens_pedido = relationship("ItemPedido", back_populates="produto")

class Pedido(Base):
    __tablename__ = "pedidos"
    id = Column(Integer, primary_key=True, index=True)
    mesa_id = Column(Integer, ForeignKey("mesas.id"), nullable=False)
    garcom_id = Column(Integer, ForeignKey("garcons.id"), nullable=False)
    status = Column(String, default="pendente")
    data_criacao = Column(DateTime, server_default=func.now())

    mesa = relationship("Mesa", back_populates="pedidos")
    garcom = relationship("Garcom", back_populates="pedidos")
    itens = relationship("ItemPedido", back_populates="pedido", cascade="all, delete-orphan")

class ItemPedido(Base):
    __tablename__ = "itens_pedido"
    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    quantidade = Column(Integer, nullable=False)

    pedido = relationship("Pedido", back_populates="itens")
    produto = relationship("Produto", back_populates="itens_pedido")
