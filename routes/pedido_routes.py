from flask import (
    render_template,
    request,
    redirect,
    session,
    flash
)

from app import app, db

from models.pedido import Pedido
from models.produto import Produto
from models.venda import Venda
from models.financeiro import Financeiro


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


@app.route("/pedidos/adicionar", methods=["POST"])
def adicionar_pedido():

    cliente = request.form.get(
        "cliente"
    )

    produto_id = int(
        request.form.get("produto_id")
    )

    quantidade = int(
        request.form.get("quantidade")
    )

    produto = Produto.query.get(
        produto_id
    )

    valor_total = (
        produto.preco * quantidade
    )

    # REDUZ ESTOQUE
    produto.estoque -= quantidade

    # PEDIDO
    novo_pedido = Pedido(
        
        cliente=cliente,
        produto_id=produto_id,
        quantidade=quantidade,
        valor_total=valor_total
    )

    # VENDA
    nova_venda = Venda(
        produto_id=produto_id,
        quantidade=quantidade,
        valor_total=valor_total
    )

    # FINANCEIRO
    financeiro = Financeiro(
        tipo="entrada",
        descricao=f"Pedido #{produto.nome}",
        valor=valor_total
    )

    db.session.add(novo_pedido)
    db.session.add(nova_venda)
    db.session.add(financeiro)

    db.session.commit()

    return redirect("/pedidos")

@app.route("/pedidos/status/<int:id>/<status>")
def atualizar_status_pedido(id, status):

    pedido = Pedido.query.get(id)

    pedido.status = status

    db.session.commit()

    return redirect("/pedidos")

@app.route("/pedidos/cancelar/<int:id>")
def cancelar_pedido(id):

    pedido = Pedido.query.get(id)

    # DEVOLVE ESTOQUE
    produto = Produto.query.get(
        pedido.produto_id
    )

    produto.estoque += pedido.quantidade

    pedido.status = "Cancelado"

    db.session.commit()

    return redirect("/pedidos")