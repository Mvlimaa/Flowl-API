from sqlalchemy.orm import Session
from . import models, schemas
from app.auth import gerar_hash_senha, verificar_senha

# Login
def criar_usuario(db: Session, usuario: schemas.UsuarioCreate):
    hashed_password = gerar_hash_senha(usuario.senha)
    db_usuario = models.Usuario(
        nome=usuario.nome,
        cpf=usuario.cpf,
        telefone=usuario.telefone,
        senha=hashed_password
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def autenticar_usuario(db: Session, cpf: str, senha: str):
    usuario = get_usuario_by_cpf(db, cpf)
    if not usuario or not verificar_senha(senha, usuario.senha):
        return None
    return usuario

def get_usuario_by_cpf(db: Session, cpf: str):
    return db.query(models.Usuario).filter(models.Usuario.cpf == cpf).first()

# Mesa
def create_mesa(db: Session, mesa: schemas.MesaCreate):
    db_mesa = models.Mesa(numero=mesa.numero, status=mesa.status or "fechada")
    db.add(db_mesa)
    db.commit()
    db.refresh(db_mesa)
    return db_mesa

def get_mesas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Mesa).offset(skip).limit(limit).all()

def get_mesas_abertas(db: Session):
    return db.query(models.Mesa).filter(models.Mesa.status == "aberta").all()

def update_status_mesa(db: Session, mesa_id: int, status: str):
    mesa = db.query(models.Mesa).filter(models.Mesa.id == mesa_id).first()
    if mesa:
        mesa.status = status
        db.commit()
        db.refresh(mesa)
    return mesa

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

def get_pedidos(db: Session):
    return db.query(models.Pedido).all()
