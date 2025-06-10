from sqlalchemy.orm import Session
from . import models, schemas

# Mesa
def create_mesa(db: Session, mesa: schemas.MesaCreate):
    db_mesa = models.Mesa(numero=mesa.numero)
    db.add(db_mesa)
    db.commit()
    db.refresh(db_mesa)
    return db_mesa

def get_mesas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Mesa).offset(skip).limit(limit).all()

def get_mesas_abertas(db: Session):
    # Mesas com pedidos com status pendente
    mesas_abertas = db.query(models.Mesa).join(models.Pedido).filter(models.Pedido.status == "pendente").distinct().all()
    return mesas_abertas

# Produto
def create_produto(db: Session, produto: schemas.ProdutoCreate):
    db_produto = models.Produto(**produto.dict())
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto

def get_produtos(db: Session):
    return db.query(models.Produto).all()

# Pedido
def create_pedido(db: Session, pedido: schemas.PedidoCreate):
    db_pedido = models.Pedido(
        mesa_id=pedido.mesa_id,
        garcom_id=pedido.garcom_id,
        status=pedido.status
    )
    db.add(db_pedido)
    db.commit()
    db.refresh(db_pedido)

    for item in pedido.itens:
        db_item = models.ItemPedido(
            pedido_id=db_pedido.id,
            produto_id=item.produto_id,
            quantidade=item.quantidade
        )
        db.add(db_item)
    db.commit()
    db.refresh(db_pedido)
    return db_pedido

def get_pedidos_por_mesa(db: Session, mesa_id: int):
    return db.query(models.Pedido).filter(models.Pedido.mesa_id == mesa_id).all()

def update_status_pedido(db: Session, pedido_id: int, status: str):
    pedido = db.query(models.Pedido).filter(models.Pedido.id == pedido_id).first()
    if pedido:
        pedido.status = status
        db.commit()
        db.refresh(pedido)
    return pedido
