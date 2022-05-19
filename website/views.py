from flask import Blueprint, flash, redirect, render_template, request, jsonify, Response
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
# essa pagina só pode ser acessada se o usuário estiver logado
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Nota muito curta!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Nota criada com sucesso!', category='sucess')
    return render_template("home.html", user=current_user)

@views.route('/edit_note/<int:id>', methods=['GET', 'POST'])
# essa pagina só pode ser acessada se o usuário estiver logado
@login_required
def edit_note(id):
    update_note = Note.query.get(id)
    if request.method == "POST":
        update_note.data = request.form.get('data')
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Ocorreu um erro durante a edição da nota"
    else:
        return render_template('edit_note.html', update_note=update_note)
    # note = Note.query.get(id)
    # if note is not None:
    #     if (request.method == 'POST'):
    #         note = request.form.get('note')
    #         if len(note) < 1:
    #             flash('Nota muito curta!', category='error')
    #         else:
    #             note = Note(data=note, user_id=current_user.id)
    #             db.session.commit()
    #             flash('Nota editada com sucesso!', category='sucess')
    #             return render_template('home.html',user=current_user, note=note)
    # else:
    #     flash('Nota não foi encontrada.', category='error')
    # return render_template('edit_note.html',user=current_user, note=note)
    # achando a nota
 
        



    
    

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})
