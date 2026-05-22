from flask import (
    jsonify,
    request
)

from app import app

from database import db

from models.produto import Produto


# LISTAR PRODUTOS
@app.route("/api/produtos")
def api_produtos():

    produtos = Produto.query.all()

    lista_produtos = []

    for produto in produtos:

        lista_produtos.append({

            "id": produto.id,
            "nome": produto.nome,
            "preco": produto.preco,
            "estoque": produto.estoque

        })

    return jsonify(lista_produtos)


# BUSCAR PRODUTO
@app.route("/api/produtos/<int:id>")
def api_produto(id):

    produto = db.session.get(
        Produto,
        id
    )

    if not produto:

        return jsonify({
            "erro": "Produto não encontrado"
        }), 404

    return jsonify({

        "id": produto.id,
        "nome": produto.nome,
        "preco": produto.preco,
        "estoque": produto.estoque

    })


# CRIAR PRODUTO
@app.route(
    "/api/produtos",
    methods=["POST"]
)
def api_criar_produto():

    dados = request.get_json()

    novo_produto = Produto(

        nome=dados["nome"],
        preco=dados["preco"],
        estoque=dados["estoque"]

    )

    db.session.add(novo_produto)

    db.session.commit()

    return jsonify({
        "mensagem": "Produto criado"
    })


# ATUALIZAR PRODUTO
@app.route(
    "/api/produtos/<int:id>",
    methods=["PUT"]
)
def api_atualizar_produto(id):

    produto = db.session.get(
        Produto,
        id
    )

    if not produto:

        return jsonify({
            "erro": "Produto não encontrado"
        }), 404

    dados = request.get_json()

    produto.nome = dados["nome"]
    produto.preco = dados["preco"]
    produto.estoque = dados["estoque"]

    db.session.commit()

    return jsonify({
        "mensagem": "Produto atualizado"
    })


# DELETAR PRODUTO
@app.route(
    "/api/produtos/<int:id>",
    methods=["DELETE"]
)
def api_deletar_produto(id):

    produto = db.session.get(
        Produto,
        id
    )

    if not produto:

        return jsonify({
            "erro": "Produto não encontrado"
        }), 404

    db.session.delete(produto)

    db.session.commit()

    return jsonify({
        "mensagem": "Produto deletado"
    })