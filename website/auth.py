from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html")


@auth.route('/logout')
def logout():
    return "<p>Logout</p>"


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    # informações a serem pegas
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # checando informações do usuário
        if len(email) < 4:
            flash('Email precisa conter mais de 4 caracteres.', category='error')
        # elif len(first_name) < 2:
            #flash('Nome precisa conter mais de 1 caracter.', category='error')
        elif password1 != password2:
            flash('Senhas diferentes.', category='error')
        elif len(password1) < 4:
            flash('Senha precisa conter mais de 4 caracteres.', category='error')
        else:
            # seguindo com a inscrição do usuário
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Conta criada com sucesso!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html")
