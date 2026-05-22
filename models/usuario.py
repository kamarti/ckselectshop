from database import db


class Usuario(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    usuario = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    senha = db.Column(
        db.String(300),
        nullable=False
    )