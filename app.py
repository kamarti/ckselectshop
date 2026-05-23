from flask import Flask

from database import configurar_banco, db


app = Flask(__name__)

configurar_banco(app)

from database import(
    db,
    configurar_banco
)

import os

app.secret_key = os.getenv(
    "SECRECT_KEY"
)

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