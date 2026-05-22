from flask import (
    render_template,
    request,
    redirect,
    session
)

from app import app

from database import db

from models.pedido import Pedido

from models.produto import Produto


# LISTAR PEDIDOS
@app.route("/pedidos")
def pedidos():

    if "usuario" not in session:

        return redirect("/login")

    pedidos = Pedido.query.order_by(
        Pedido.id.desc()
    ).all()

    produtos = Produto.query.all()

    return render_template(
        "pedidos.html",
        pedidos=pedidos,
        produtos=produtos
    )


# CRIAR PEDIDO
@app.route(
    "/pedidos/criar",
    methods=["POST"]
)
def criar_pedido():

    cliente = request.form.get(
        "cliente"
    )

    produto_id = int(
        request.form.get("produto_id")
    )

    quantidade = int(
        request.form.get("quantidade")
    )

    produto = db.session.get(
        Produto,
        produto_id
    )

    valor_total = (
        produto.preco * quantidade
    )

    novo_pedido = Pedido(

        cliente=cliente,
        produto=produto.nome,
        quantidade=quantidade,
        valor_total=valor_total

    )

    db.session.add(novo_pedido)

    db.session.commit()

    return redirect("/pedidos")


# ALTERAR STATUS
@app.route(
    "/pedidos/status/<int:id>"
)
def alterar_status(id):

    pedido = db.session.get(
        Pedido,
        id
    )

    if pedido.status == "Pendente":

        pedido.status = "Pago"

    elif pedido.status == "Pago":

        pedido.status = "Enviado"

    elif pedido.status == "Enviado":

        pedido.status = "Entregue"

    db.session.commit()

    return redirect("/pedidos")