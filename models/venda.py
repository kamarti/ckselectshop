from database import db
from datetime import datetime

class Venda(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    produto_id = db.Column(
        db.Integer,
        db.ForeignKey('produto.id'),
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

    data = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    produto = db.relationship(
        'Produto',
        backref='vendas'
    )