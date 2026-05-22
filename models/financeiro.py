from database import db

class Financeiro(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    tipo = db.Column(
        db.String(20),
        nullable=False
    )

    descricao = db.Column(
        db.String(200),
        nullable=False
    )

    valor = db.Column(
        db.Float,
        nullable=False
    )