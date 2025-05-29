from flask import Blueprint, render_template, request,redirect,url_for
from db import inserir_usuario

cadastro_route = Blueprint('cadastro', __name__)

@cadastro_route.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    mensagem = ""
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        perfil = request.form['perfil']

        sucesso, mensagem = inserir_usuario(nome, email, senha, perfil)

    return render_template('cadastro.html', mensagem=mensagem)



@cadastro_route.route('/listar_cadastro')
def listar_cadastro():
    return redirect(url_for('cadastro.cadastro'))
    