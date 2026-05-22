from database import db


class Pedido(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    cliente = db.Column(
        db.String(150),
        nullable=False
    )

    produto = db.Column(
        db.String(150),
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