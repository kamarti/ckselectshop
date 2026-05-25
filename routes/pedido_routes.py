from flask import (
    render_template,
    request,
    redirect,
    session,
    flash
)

from app import app
from database import db

from models.pedido import Pedido
from models.produto import Produto
from models.venda import Venda
from models.financeiro import Financeiro


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


# ADICIONAR PEDIDO
@app.route(
    "/pedidos/adicionar",
    methods=["POST"]
)
def adicionar_pedido():

    if "usuario" not in session:

        return redirect("/login")

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

    # VALIDAR PRODUTO
    if not produto:

        flash("Produto não encontrado.")

        return redirect("/pedidos")

    # VALIDAR ESTOQUE
    if produto.estoque < quantidade:

        flash("Estoque insuficiente.")

        return redirect("/pedidos")

    valor_total = (
        produto.preco * quantidade
    )

    # REDUZIR ESTOQUE
    produto.estoque -= quantidade

    # NOVO PEDIDO
    novo_pedido = Pedido(

        cliente=cliente,
        produto_id=produto_id,
        quantidade=quantidade,
        valor_total=valor_total,
        status="Pendente"
    )

    # NOVA VENDA
    nova_venda = Venda(

        produto_id=produto_id,
        quantidade=quantidade,
        valor_total=valor_total
    )

    # FINANCEIRO
    financeiro = Financeiro(

        tipo="entrada",
        descricao=f"Pedido de {produto.nome}",
        valor=valor_total
    )

    db.session.add(novo_pedido)

    db.session.add(nova_venda)

    db.session.add(financeiro)

    db.session.commit()

    flash("Pedido criado com sucesso.")

    return redirect("/pedidos")


# ATUALIZAR STATUS
@app.route("/pedidos/status/<int:id>/<status>")
def atualizar_status_pedido(id, status):

    if "usuario" not in session:

        return redirect("/login")

    pedido = db.session.get(
        Pedido,
        id
    )

    if not pedido:

        flash("Pedido não encontrado.")

        return redirect("/pedidos")

    status_permitidos = [
        "Pendente",
        "Enviado",
        "Entregue",
        "Cancelado"
    ]

    if status not in status_permitidos:

        flash("Status inválido.")

        return redirect("/pedidos")

    pedido.status = status

    db.session.commit()

    flash("Status atualizado.")

    return redirect("/pedidos")


# CANCELAR PEDIDO
@app.route("/pedidos/cancelar/<int:id>")
def cancelar_pedido(id):

    if "usuario" not in session:

        return redirect("/login")

    pedido = db.session.get(
        Pedido,
        id
    )

    if not pedido:

        flash("Pedido não encontrado.")

        return redirect("/pedidos")

    # EVITAR CANCELAR DUAS VEZES
    if pedido.status == "Cancelado":

        flash("Pedido já cancelado.")

        return redirect("/pedidos")

    produto = db.session.get(
        Produto,
        pedido.produto_id
    )

    # DEVOLVER ESTOQUE
    produto.estoque += pedido.quantidade

    pedido.status = "Cancelado"

    db.session.commit()

    flash("Pedido cancelado.")

    return redirect("/pedidos")