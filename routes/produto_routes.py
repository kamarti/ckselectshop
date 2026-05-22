from flask import (
    render_template,
    request,
    redirect,
    session
)

from app import app

from database import db

from models.produto import Produto
from models.financeiro import Financeiro
from models.venda import Venda


# HOME
@app.route("/")
def home():

    # VERIFICAR LOGIN
    if "usuario" not in session:

        return redirect("/login")

    # PRODUTOS
    produtos = Produto.query.order_by(
        Produto.id.desc()
    ).all()

    # CARDS DASHBOARD
    total_produtos = len(produtos)

    total_estoque = sum(
        produto.estoque
        for produto in produtos
    )

    valor_total_estoque = sum(
        produto.preco * produto.estoque
        for produto in produtos
    )

    estoque_baixo = len([
        produto
        for produto in produtos
        if produto.estoque <= 5
    ])

    # FINANCEIRO
    registros_financeiros = Financeiro.query.all()

    total_entradas = sum(
        registro.valor
        for registro in registros_financeiros
        if registro.tipo == "entrada"
    )

    total_saidas = sum(
        registro.valor
        for registro in registros_financeiros
        if registro.tipo == "saida"
    )

    saldo_total = total_entradas - total_saidas

    # VENDAS
    vendas = Venda.query.all()

    produtos_vendidos = {}

    for venda in vendas:

        nome_produto = venda.produto.nome

        if nome_produto not in produtos_vendidos:

            produtos_vendidos[nome_produto] = 0

        produtos_vendidos[nome_produto] += venda.quantidade

    nomes_vendas = list(
        produtos_vendidos.keys()
    )

    quantidade_vendas = list(
        produtos_vendidos.values()
    )

    # GRÁFICO ESTOQUE
    nomes_produtos = [
        produto.nome
        for produto in produtos
    ]

    estoques = [
        produto.estoque
        for produto in produtos
    ]

    return render_template(
        "index.html",

        produtos=produtos,

        total_produtos=total_produtos,
        total_estoque=total_estoque,
        valor_total_estoque=valor_total_estoque,
        estoque_baixo=estoque_baixo,

        nomes_produtos=nomes_produtos,
        estoques=estoques,

        total_entradas=total_entradas,
        total_saidas=total_saidas,
        saldo_total=saldo_total,

        nomes_vendas=nomes_vendas,
        quantidade_vendas=quantidade_vendas
    )


# ADICIONAR PRODUTO
@app.route("/adicionar", methods=["POST"])
def adicionar():

    nome = request.form.get("nome")

    preco = float(
        request.form.get("preco")
    )

    estoque = int(
        request.form.get("estoque")
    )

    novo_produto = Produto(
        nome=nome,
        preco=preco,
        estoque=estoque
    )

    db.session.add(novo_produto)

    db.session.commit()

    return redirect("/")


# EDITAR PRODUTO
@app.route("/editar/<int:id>")
def editar(id):

    produto = db.session.get(
        Produto,
        id
    )

    return render_template(
        "editar.html",
        produto=produto
    )


# ATUALIZAR PRODUTO
@app.route("/atualizar/<int:id>", methods=["POST"])
def atualizar(id):

    produto = db.session.get(
        Produto,
        id
    )

    produto.nome = request.form.get("nome")

    produto.preco = float(
        request.form.get("preco")
    )

    produto.estoque = int(
        request.form.get("estoque")
    )

    db.session.commit()

    return redirect("/")


# DELETAR PRODUTO
@app.route("/deletar/<int:id>")
def deletar(id):

    produto = db.session.get(
        Produto,
        id
    )

    db.session.delete(produto)

    db.session.commit()

    return redirect("/")

from flask import send_file

from reportlab.pdfgen import canvas


# GERAR PDF PRODUTOS
@app.route("/relatorio/produtos")
def relatorio_produtos():

    if "usuario" not in session:

        return redirect("/login")

    produtos = Produto.query.all()

    caminho_pdf = "relatorios/produtos.pdf"

    pdf = canvas.Canvas(caminho_pdf)

    pdf.setFont("Helvetica-Bold", 18)

    pdf.drawString(
        200,
        800,
        "Relatório de Produtos"
    )

    y = 750

    pdf.setFont("Helvetica", 12)

    for produto in produtos:

        texto = (
            f"ID: {produto.id} | "
            f"Produto: {produto.nome} | "
            f"Preço: R$ {produto.preco} | "
            f"Estoque: {produto.estoque}"
        )

        pdf.drawString(
            50,
            y,
            texto
        )

        y -= 25

    pdf.save()

    return send_file(
        caminho_pdf,
        as_attachment=True
    )