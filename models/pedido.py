from datetime import datetime

from database import db


class Pedido(db.Model):

    __tablename__ = "pedidos"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    cliente = db.Column(
        db.String(200),
        nullable=False
    )

    produto_id = db.Column(
        db.Integer,
        db.ForeignKey("produto.id"),
        nullable=False
    )

    quantidade = db.Column(
        db.Integer,
        nullable=False
    )

    valor_total = db.Column(
        db.Float,
        nullable=False
    )

    status = db.Column(
        db.String(50),
        default="Pendente"
    )

    data = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    produto = db.relationship(
        "Produto",
        backref=db.backref(
            "pedidos",
            lazy=True
        )
    )