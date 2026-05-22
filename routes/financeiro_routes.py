from flask import (
    render_template,
    request,
    redirect,
    session
)

from app import app, db

from models.financeiro import Financeiro


@app.route("/financeiro")
def financeiro():

    if "usuario" not in session:

        return redirect("/login")

    registros = Financeiro.query.all()

    entradas = sum(
        r.valor
        for r in registros
        if r.tipo == "entrada"
    )

    saidas = sum(
        r.valor
        for r in registros
        if r.tipo == "saida"
    )

    saldo = entradas - saidas

    return render_template(
        "financeiro.html",
        registros=registros,
        entradas=entradas,
        saidas=saidas,
        saldo=saldo
    )


@app.route(
    "/financeiro/adicionar",
    methods=["POST"]
)
def adicionar_financeiro():

    tipo = request.form.get("tipo")

    descricao = request.form.get("descricao")

    valor = float(request.form.get("valor"))

    novo_registro = Financeiro(
        tipo=tipo,
        descricao=descricao,
        valor=valor
    )

    db.session.add(novo_registro)

    db.session.commit()

    return redirect("/financeiro")