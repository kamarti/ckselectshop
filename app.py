from flask import Flask
from database import db
import os

# CRIAR APP
app = Flask(__name__)

# CONFIGURAÇÕES
app.config["SECRET_KEY"] = "ckselectshop"

# SQLITE
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///banco.db"

# DESATIVAR WARNING
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# PASTA UPLOADS
app.config["UPLOAD_FOLDER"] = "static/uploads"

# GARANTIR PASTAS
os.makedirs("static/uploads", exist_ok=True)
os.makedirs("relatorios", exist_ok=True)

# INICIAR BANCO
db.init_app(app)

# IMPORTAR MODELS
from models.produto import Produto
from models.financeiro import Financeiro
from models.venda import Venda
from models.pedido import Pedido
from models.usuario import Usuario
from models.estoque import MovimentacaoEstoque

# IMPORTAR ROTAS
import routes.produto_routes
import routes.financeiro_routes
import routes.venda_routes
import routes.pedido_routes
import routes.estoque_routes
import routes.auth_routes
import routes.api_routes

# CRIAR TABELAS
with app.app_context():

    db.create_all()

# RODAR APP
if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )