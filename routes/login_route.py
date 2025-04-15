from flask import Blueprint, render_template, request, redirect, url_for, session
from db import buscar_usuario_por_email
import bcrypt

login_route = Blueprint('login_route', __name__)

@login_route.route('/login', methods=['GET', 'POST'])
def login():
    mensagem = ""
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        usuario = buscar_usuario_por_email(email)

        if usuario and bcrypt.checkpw(senha.encode('utf-8'), usuario[3].encode('utf-8')):
            session['usuario_id'] = usuario[0]
            session['nome'] = usuario[1]
            session['perfil'] = usuario[4]
            return redirect(url_for('inicial_route.inicial'))
        else:
            mensagem = "Email ou senha incorretos."
    return render_template('login.html', mensagem=mensagem)
