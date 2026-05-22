from flask import (
    render_template,
    request,
    redirect,
    session
)

from app import app

from database import db

from models.produto import Produto
from models.estoque import MovimentacaoEstoque


# PÁGINA ESTOQUE
@app.route("/estoque")
def estoque():

    if "usuario" not in session:

        return redirect("/login")

    produtos = Produto.query.all()

    movimentacoes = (
        MovimentacaoEstoque.query
        .order_by(MovimentacaoEstoque.id.desc())
        .all()
    )

    return render_template(
        "estoque.html",
        produtos=produtos,
        movimentacoes=movimentacoes
    )


# MOVIMENTAR ESTOQUE
@app.route(
    "/estoque/movimentar",
    methods=["POST"]
)
def movimentar_estoque():

    produto_id = int(
        request.form.get("produto_id")
    )

    tipo = request.form.get("tipo")

    quantidade = int(
        request.form.get("quantidade")
    )

    produto = db.session.get(
        Produto,
        produto_id
    )

    # ENTRADA
    if tipo == "entrada":

        produto.estoque += quantidade

    # SAÍDA
    elif tipo == "saida":

        if produto.estoque < quantidade:

            return "Erro: estoque insuficiente"

        produto.estoque -= quantidade

    movimentacao = MovimentacaoEstoque(
        produto_id=produto_id,
        tipo=tipo,
        quantidade=quantidade
    )

    db.session.add(movimentacao)

    db.session.commit()

    return redirect("/estoque")