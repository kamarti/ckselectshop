from database import db
from datetime import datetime

class MovimentacaoEstoque(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    produto_id = db.Column(
        db.Integer,
        db.ForeignKey('produto.id'),
        nullable=False
    )

    tipo = db.Column(
        db.String(20),
        nullable=False
    )

    quantidade = db.Column(
        db.Integer,
        nullable=False
    )

    data = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    produto = db.relationship(
        'Produto',
        backref='movimentacoes'
    )