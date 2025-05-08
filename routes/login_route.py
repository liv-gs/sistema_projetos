from flask import Blueprint, render_template, request, redirect, url_for, session
from db import buscar_usuario_por_email,conectar

login_route = Blueprint('login_route', __name__)

@login_route.route('/login', methods=['GET', 'POST'])
def login():
    mensagem = ""
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        
        conn = conectar() 
        usuario = buscar_usuario_por_email(conn, email)

        if usuario and senha == usuario['senha']:
            session['usuario_id'] = usuario['id']
            session['nome'] = usuario['nome']
            session['perfil'] = usuario['perfil']
            return redirect(url_for('inicial_route.inicial'))
        else:
            mensagem = "Email ou senha incorretos."

    return render_template('login.html', mensagem=mensagem)
