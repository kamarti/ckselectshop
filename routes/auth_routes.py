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
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        usuario_digitado = request.form.get(
            "usuario"
        )

        senha_digitada = request.form.get(
            "senha"
        )

        usuario = Usuario.query.filter_by(
            usuario=usuario_digitado
        ).first()

        if usuario and check_password_hash(
            usuario.senha,
            senha_digitada
        ):

            session["usuario"] = usuario.usuario

            return redirect("/")

        return "Usuário ou senha inválidos"

    return render_template("login.html")


# CADASTRO
@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():

    if request.method == "POST":

        usuario = request.form.get("usuario")

        senha = request.form.get("senha")

        senha_hash = generate_password_hash(
            senha
        )

        novo_usuario = Usuario(
            usuario=usuario,
            senha=senha_hash
        )

        db.session.add(novo_usuario)

        db.session.commit()

        return redirect("/login")

    return render_template(
        "cadastro.html"
    )


# LOGOUT
@app.route("/logout")
def logout():

    session.pop("usuario", None)

    return redirect("/login")