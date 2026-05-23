import os

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def configurar_banco(app):

    database_url = os.getenv(
        "DATABASE_URL"
    )

    if database_url:

        database_url = database_url.replace(
            "postgres://",
            "postgresql://",
            1
        )

        app.config[
            "SQLALCHEMY_DATABASE_URI"
        ] = database_url

    else:

        app.config[
            "SQLALCHEMY_DATABASE_URI"
        ] = "sqlite:///database.db"

    app.config[
        "SQLALCHEMY_TRACK_MODIFICATIONS"
    ] = False

    db.init_app(app)