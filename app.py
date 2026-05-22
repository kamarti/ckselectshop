from flask import Flask

from database import db


app = Flask(__name__)

app.secret_key = "erp_loja_secret"

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:///database.db"
)

db.init_app(app)


# IMPORTAR MODELS
from models.produto import Produto
from models.financeiro import Financeiro
from models.estoque import MovimentacaoEstoque
from models.venda import Venda
from models.usuario import Usuario
from models.pedido import Pedido


# IMPORTAR ROTAS
from routes.auth_routes import *
from routes.produto_routes import *
from routes.financeiro_routes import *
from routes.estoque_routes import *
from routes.venda_routes import *
from routes.api_routes import *
from routes.pedido_routes import *


with app.app_context():

    db.create_all()


if __name__ == "__main__":

    app.run(debug=True)