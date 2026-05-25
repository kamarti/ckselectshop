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

    produtos = Produto.query.order_by(
        Produto.id.desc()
    ).all()

    lista_produtos = []

    for produto in produtos:

        lista_produtos.append({

            "id": produto.id,
            "nome": produto.nome,
            "preco": produto.preco,
            "estoque": produto.estoque,
            "imagem": produto.imagem

        })

    return jsonify(lista_produtos), 200


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
        "estoque": produto.estoque,
        "imagem": produto.imagem

    }), 200


# CRIAR PRODUTO
@app.route(
    "/api/produtos",
    methods=["POST"]
)
def api_criar_produto():

    dados = request.get_json()

    # VALIDAR JSON
    if not dados:

        return jsonify({

            "erro": "JSON inválido"

        }), 400

    nome = dados.get("nome")

    preco = dados.get("preco")

    estoque = dados.get("estoque")

    # VALIDAR CAMPOS
    if not nome or preco is None or estoque is None:

        return jsonify({

            "erro": "Campos obrigatórios ausentes"

        }), 400

    try:

        preco = float(preco)

        estoque = int(estoque)

    except ValueError:

        return jsonify({

            "erro": "Preço ou estoque inválido"

        }), 400

    novo_produto = Produto(

        nome=nome,
        preco=preco,
        estoque=estoque
    )

    db.session.add(
        novo_produto
    )

    db.session.commit()

    return jsonify({

        "mensagem": "Produto criado com sucesso",
        "id": novo_produto.id

    }), 201


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

    # VALIDAR JSON
    if not dados:

        return jsonify({

            "erro": "JSON inválido"

        }), 400

    nome = dados.get("nome")

    preco = dados.get("preco")

    estoque = dados.get("estoque")

    # ATUALIZAR SOMENTE SE INFORMADO
    if nome:

        produto.nome = nome

    if preco is not None:

        try:

            produto.preco = float(preco)

        except ValueError:

            return jsonify({

                "erro": "Preço inválido"

            }), 400

    if estoque is not None:

        try:

            produto.estoque = int(estoque)

        except ValueError:

            return jsonify({

                "erro": "Estoque inválido"

            }), 400

    db.session.commit()

    return jsonify({

        "mensagem": "Produto atualizado com sucesso"

    }), 200


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

    db.session.delete(
        produto
    )

    db.session.commit()

    return jsonify({

        "mensagem": "Produto deletado com sucesso"

    }), 200