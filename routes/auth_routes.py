from flask import (
    render_template,
    request,
    redirect,
    session,
    flash
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from app import app
from database import db

from models.usuario import Usuario


# LOGIN
@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    # SE JÁ ESTIVER LOGADO
    if "usuario" in session:

        return redirect("/")

    if request.method == "POST":

        usuario_digitado = request.form.get(
            "usuario"
        )

        senha_digitada = request.form.get(
            "senha"
        )

        # VALIDAR CAMPOS
        if not usuario_digitado or not senha_digitada:

            flash("Preencha todos os campos.")

            return redirect("/login")

        usuario = Usuario.query.filter_by(
            usuario=usuario_digitado
        ).first()

        # VALIDAR LOGIN
        if usuario and check_password_hash(
            usuario.senha,
            senha_digitada
        ):

            session["usuario"] = usuario.usuario

            flash("Login realizado com sucesso.")

            return redirect("/")

        flash("Usuário ou senha inválidos.")

        return redirect("/login")

    return render_template(
        "login.html"
    )


# CADASTRO
@app.route(
    "/cadastro",
    methods=["GET", "POST"]
)
def cadastro():

    if request.method == "POST":

        usuario = request.form.get(
            "usuario"
        )

        senha = request.form.get(
            "senha"
        )

        # VALIDAR CAMPOS
        if not usuario or not senha:

            flash("Preencha todos os campos.")

            return redirect("/cadastro")

        # VERIFICAR USUÁRIO EXISTENTE
        usuario_existente = Usuario.query.filter_by(
            usuario=usuario
        ).first()

        if usuario_existente:

            flash("Usuário já cadastrado.")

            return redirect("/cadastro")

        # CRIPTOGRAFAR SENHA
        senha_hash = generate_password_hash(
            senha
        )

        novo_usuario = Usuario(

            usuario=usuario,
            senha=senha_hash
        )

        db.session.add(
            novo_usuario
        )

        db.session.commit()

        flash("Cadastro realizado com sucesso.")

        return redirect("/login")

    return render_template(
        "cadastro.html"
    )


# LOGOUT
@app.route("/logout")
def logout():

    session.pop(
        "usuario",
        None
    )

    flash("Logout realizado com sucesso.")

    return redirect("/login")