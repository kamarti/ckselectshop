from flask import (
    render_template,
    request,
    redirect,
    session,
    flash
)

from app import app
from database import db

from models.financeiro import Financeiro


# PÁGINA FINANCEIRO
@app.route("/financeiro")
def financeiro():

    if "usuario" not in session:

        return redirect("/login")

    registros = (
        Financeiro.query
        .order_by(Financeiro.id.desc())
        .all()
    )

    entradas = sum(
        registro.valor
        for registro in registros
        if registro.tipo == "entrada"
    )

    saidas = sum(
        registro.valor
        for registro in registros
        if registro.tipo == "saida"
    )

    saldo = entradas - saidas

    return render_template(
        "financeiro.html",

        registros=registros,

        entradas=entradas,
        saidas=saidas,
        saldo=saldo
    )


# ADICIONAR REGISTRO FINANCEIRO
@app.route(
    "/financeiro/adicionar",
    methods=["POST"]
)
def adicionar_financeiro():

    if "usuario" not in session:

        return redirect("/login")

    tipo = request.form.get(
        "tipo"
    )

    descricao = request.form.get(
        "descricao"
    )

    valor = request.form.get(
        "valor"
    )

    # VALIDAR CAMPOS
    if not tipo or not descricao or not valor:

        flash("Preencha todos os campos.")

        return redirect("/financeiro")

    try:

        valor = float(valor)

    except ValueError:

        flash("Valor inválido.")

        return redirect("/financeiro")

    # VALIDAR TIPO
    tipos_permitidos = [
        "entrada",
        "saida"
    ]

    if tipo not in tipos_permitidos:

        flash("Tipo inválido.")

        return redirect("/financeiro")

    novo_registro = Financeiro(

        tipo=tipo,
        descricao=descricao,
        valor=valor
    )

    db.session.add(
        novo_registro
    )

    db.session.commit()

    flash("Registro financeiro adicionado com sucesso.")

    return redirect("/financeiro")