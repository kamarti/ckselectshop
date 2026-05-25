from flask import (
    render_template,
    request,
    redirect,
    session,
    flash
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

    produtos = Produto.query.order_by(
        Produto.nome.asc()
    ).all()

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

    if "usuario" not in session:

        return redirect("/login")

    produto_id = request.form.get(
        "produto_id"
    )

    tipo = request.form.get(
        "tipo"
    )

    quantidade = request.form.get(
        "quantidade"
    )

    # VALIDAR CAMPOS
    if not produto_id or not tipo or not quantidade:

        flash("Preencha todos os campos.")

        return redirect("/estoque")

    try:

        produto_id = int(produto_id)

        quantidade = int(quantidade)

    except ValueError:

        flash("Valores inválidos.")

        return redirect("/estoque")

    produto = db.session.get(
        Produto,
        produto_id
    )

    # VALIDAR PRODUTO
    if not produto:

        flash("Produto não encontrado.")

        return redirect("/estoque")

    # VALIDAR TIPO
    tipos_permitidos = [
        "entrada",
        "saida"
    ]

    if tipo not in tipos_permitidos:

        flash("Tipo de movimentação inválido.")

        return redirect("/estoque")

    # VALIDAR QUANTIDADE
    if quantidade <= 0:

        flash("Quantidade deve ser maior que zero.")

        return redirect("/estoque")

    # ENTRADA
    if tipo == "entrada":

        produto.estoque += quantidade

    # SAÍDA
    elif tipo == "saida":

        if produto.estoque < quantidade:

            flash("Estoque insuficiente.")

            return redirect("/estoque")

        produto.estoque -= quantidade

    # MOVIMENTAÇÃO
    movimentacao = MovimentacaoEstoque(

        produto_id=produto_id,
        tipo=tipo,
        quantidade=quantidade
    )

    db.session.add(
        movimentacao
    )

    db.session.commit()

    flash("Movimentação realizada com sucesso.")

    return redirect("/estoque")