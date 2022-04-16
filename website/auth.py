from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # checar se as informações são válidas
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Login realizado com sucesso!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Algo está errado, tente novamente.', category='error')
    return render_template("login.html", user=current_user)


@auth.route('/logout')
# essa pagina só pode ser acessada se o usuário estiver logado
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    # informações a serem pegas
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # checando se o usuário já existe
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Esse emaill já foi cadastrdo.', category='error')

        # checando informações do usuário
        elif len(email) < 4:
            flash('Email precisa conter mais de 4 caracteres.', category='error')
        elif len(first_name) < 2:
            flash('Nome precisa conter mais de 1 caracter.', category='error')
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
            login_user(user, remember=True)
            flash('Conta criada com sucesso!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
