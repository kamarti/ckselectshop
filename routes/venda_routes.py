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
from models.venda import Venda
from models.financeiro import Financeiro
from models.estoque import MovimentacaoEstoque


# PÁGINA VENDAS
@app.route("/vendas")
def vendas():

    if "usuario" not in session:

        return redirect("/login")

    produtos = Produto.query.all()

    vendas = (
        Venda.query
        .order_by(Venda.id.desc())
        .all()
    )

    return render_template(
        "vendas.html",
        produtos=produtos,
        vendas=vendas
    )


# REGISTRAR VENDA
@app.route(
    "/vendas/registrar",
    methods=["POST"]
)
def registrar_venda():

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

    # VALIDAR ESTOQUE
    if produto.estoque < quantidade:

        return "Erro: estoque insuficiente"

    valor_total = (
        produto.preco * quantidade
    )

    # REDUZ ESTOQUE
    produto.estoque -= quantidade

    # VENDA
    venda = Venda(
        produto_id=produto_id,
        quantidade=quantidade,
        valor_total=valor_total
    )

    db.session.add(venda)

    # MOVIMENTAÇÃO
    movimentacao = MovimentacaoEstoque(
        produto_id=produto_id,
        tipo="saida",
        quantidade=quantidade
    )

    db.session.add(movimentacao)

    # FINANCEIRO
    financeiro = Financeiro(
        tipo="entrada",
        descricao=f"Venda de {produto.nome}",
        valor=valor_total
    )

    db.session.add(financeiro)

    db.session.commit()

    return redirect("/vendas")