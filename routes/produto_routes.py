from flask import (
    render_template,
    request,
    redirect,
    session,
    flash,
    send_file
)

from werkzeug.utils import secure_filename

import os

from app import app

from database import db

from models.produto import Produto
from models.financeiro import Financeiro
from models.venda import Venda
from models.pedido import Pedido

from reportlab.pdfgen import canvas


# HOME
@app.route("/")
def home():

    # VERIFICAR LOGIN
    if "usuario" not in session:

        return redirect("/login")

    # BUSCA
    busca = request.args.get(
        "busca"
    )

    filtro = request.args.get(
        "filtro"
    )

    query = Produto.query

    # FILTRO BUSCA
    if busca:

        query = query.filter(
            Produto.nome.ilike(
                f"%{busca}%"
            )
        )

    # FILTRO ESTOQUE BAIXO
    if filtro == "baixo":

        query = query.filter(
            Produto.estoque <= 5
        )

    # PAGINAÇÃO
    pagina = request.args.get(
        "pagina",
        1,
        type=int
    )

    produtos = query.order_by(
        Produto.id.desc()
    ).paginate(
        page=pagina,
        per_page=10
    )

    # DASHBOARD
    total_produtos = Produto.query.count()

    todos_produtos = Produto.query.all()

    total_estoque = sum(
        produto.estoque
        for produto in todos_produtos
    )

    valor_total_estoque = sum(
        produto.preco * produto.estoque
        for produto in todos_produtos
    )

    estoque_baixo = len([
        produto
        for produto in todos_produtos
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

    saldo_total = (
        total_entradas - total_saidas
    )

    # VENDAS
    vendas = Venda.query.all()

    produtos_vendidos = {}

    for venda in vendas:

        if venda.produto:

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
        for produto in produtos.items
    ]

    estoques = [
        produto.estoque
        for produto in produtos.items
    ]

    # PEDIDOS
    total_pedidos = len(vendas)

    pedidos_pendentes = Pedido.query.filter_by(
        status="Pendente"
    ).count()

    # TICKET MÉDIO
    if total_pedidos > 0:

        ticket_medio = (
            saldo_total / total_pedidos
        )

    else:

        ticket_medio = 0

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
        quantidade_vendas=quantidade_vendas,

        total_pedidos=total_pedidos,
        pedidos_pendentes=pedidos_pendentes,
        ticket_medio=ticket_medio
    )


# ADICIONAR PRODUTO
@app.route(
    "/adicionar",
    methods=["POST"]
)
def adicionar():

    try:

        nome = request.form.get(
            "nome"
        )

        preco = float(
            request.form.get("preco")
        )

        estoque = int(
            request.form.get("estoque")
        )

        imagem = request.files.get(
            "imagem"
        )

        extensoes_permitidas = [
            "png",
            "jpg",
            "jpeg",
            "webp"
        ]

        nome_arquivo = None

        # VALIDAR IMAGEM
        if imagem and imagem.filename != "":

            extensao = (
                imagem.filename
                .split(".")[-1]
                .lower()
            )

            if extensao not in extensoes_permitidas:

                flash(
                    "Formato de imagem inválido.",
                    "danger"
                )

                return redirect("/")

            nome_arquivo = secure_filename(
                imagem.filename
            )

            os.makedirs(
                "static/uploads",
                exist_ok=True
            )

            caminho = os.path.join(
                "static/uploads",
                nome_arquivo
            )

            imagem.save(caminho)

        novo_produto = Produto(

            nome=nome,
            preco=preco,
            estoque=estoque,
            imagem=nome_arquivo
        )

        db.session.add(
            novo_produto
        )

        db.session.commit()

        flash(
            "Produto cadastrado com sucesso!",
            "success"
        )

    except Exception as erro:

        db.session.rollback()

        print(erro)

        flash(
            "Erro ao cadastrar produto.",
            "danger"
        )

    return redirect("/")


# EDITAR PRODUTO
@app.route("/editar/<int:id>")
def editar(id):

    if "usuario" not in session:

        return redirect("/login")

    produto = db.session.get(
        Produto,
        id
    )

    if not produto:

        flash(
            "Produto não encontrado.",
            "danger"
        )

        return redirect("/")

    return render_template(
        "editar.html",
        produto=produto
    )


# ATUALIZAR PRODUTO
@app.route(
    "/atualizar/<int:id>",
    methods=["POST"]
)
def atualizar(id):

    try:

        produto = db.session.get(
            Produto,
            id
        )

        if not produto:

            flash(
                "Produto não encontrado.",
                "danger"
            )

            return redirect("/")

        produto.nome = request.form.get(
            "nome"
        )

        produto.preco = float(
            request.form.get("preco")
        )

        produto.estoque = int(
            request.form.get("estoque")
        )

        db.session.commit()

        flash(
            "Produto atualizado com sucesso!",
            "success"
        )

    except Exception as erro:

        db.session.rollback()

        print(erro)

        flash(
            "Erro ao atualizar produto.",
            "danger"
        )

    return redirect("/")


# DELETAR PRODUTO
@app.route("/deletar/<int:id>")
def deletar(id):

    try:

        produto = db.session.get(
            Produto,
            id
        )

        if not produto:

            flash(
                "Produto não encontrado.",
                "danger"
            )

            return redirect("/")

        db.session.delete(produto)

        db.session.commit()

        flash(
            "Produto excluído com sucesso!",
            "success"
        )

    except Exception as erro:

        db.session.rollback()

        print(erro)

        flash(
            "Erro ao excluir produto.",
            "danger"
        )

    return redirect("/")


# GERAR PDF PRODUTOS
@app.route("/relatorio/produtos")
def relatorio_produtos():

    if "usuario" not in session:

        return redirect("/login")

    try:

        produtos = Produto.query.all()

        os.makedirs(
            "relatorios",
            exist_ok=True
        )

        caminho_pdf = (
            "relatorios/produtos.pdf"
        )

        pdf = canvas.Canvas(
            caminho_pdf
        )

        pdf.setFont(
            "Helvetica-Bold",
            18
        )

        pdf.drawString(
            180,
            800,
            "Relatório de Produtos"
        )

        y = 750

        pdf.setFont(
            "Helvetica",
            12
        )

        for produto in produtos:

            texto = (
                f"ID: {produto.id} | "
                f"Produto: {produto.nome} | "
                f"Preço: R$ {produto.preco:.2f} | "
                f"Estoque: {produto.estoque}"
            )

            pdf.drawString(
                50,
                y,
                texto
            )

            y -= 25

            # NOVA PÁGINA
            if y <= 50:

                pdf.showPage()

                y = 750

        pdf.save()

        return send_file(
            caminho_pdf,
            as_attachment=True
        )

    except Exception as erro:

        print(erro)

        flash(
            "Erro ao gerar relatório.",
            "danger"
        )

        return redirect("/")