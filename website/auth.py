from flask import Blueprint, render_template, request, flash

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
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # checando informações do usuário
        if len(email) < 4:
            flash('Email precisa conter mais de 4 caracteres.', category='error')
        elif len(firstName) < 2:
            flash('Nome precisa conter mais de 1 caracter.', category='error')
        elif password1 != password2:
            flash('Senhas diferentes.', category='error')
        elif len(password1) < 4:
            flash('Senha precisa conter mais de 4 caracteres.', category='error')
        else:
            # seguindo com a inscrição do usuário
            flash('Conta criada com sucesso!', category='success')

    return render_template("sign_up.html")
