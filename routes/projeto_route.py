from flask import Blueprint, render_template, request, redirect, url_for
from db import salvar_projeto, buscar_projeto, excluir_projeto, buscar_projeto_por_id, atualizar_projeto

projeto_route = Blueprint('projeto_route', __name__)


@projeto_route.route('/projeto', methods=['GET', 'POST'])
def listar_projetos():
    if request.method == 'POST':  # Salva projeto
        nome = request.form['nome']
        descricao = request.form['descricao']
        data_inicio = request.form['data_inicio']
        data_fim = request.form['data_fim']
        responsavel = request.form['responsavel']  # Responsável
        equipe = request.form['equipe']  # Equipe

        salvar_projeto(nome, descricao, data_inicio, data_fim, responsavel, equipe)
        return redirect(url_for('projeto_route.listar_projetos'))  # Redireciona após salvar

    projetos = buscar_projeto()  # Busca os projetos do banco
    return render_template('projeto.html', projetos=projetos)  # Renderiza o HTML com os projetos


@projeto_route.route('/projeto/excluir/<int:id>', methods=['POST'])
def excluir_projeto_route(id):
    excluir_projeto(id)  # Exclui o projeto pelo ID
    return redirect(url_for('projeto_route.listar_projetos'))  # Redireciona para a lista


@projeto_route.route('/projeto/editar/<int:id>', methods=['GET', 'POST'])
def editar_projeto(id):
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        data_inicio = request.form['data_inicio']
        data_fim = request.form['data_fim']
        responsavel = request.form['responsavel']  # Responsável
        equipe = request.form['equipe']  # Equipe

        atualizar_projeto(id, nome, descricao, data_inicio, data_fim, responsavel, equipe)
        return redirect(url_for('projeto_route.listar_projetos'))  # Redireciona após editar

    projeto = buscar_projeto_por_id(id)  # Busca o projeto para edição
    return render_template('projeto.html', projeto_editar=projeto, projetos=buscar_projeto())  # Passa o projeto e todos os projetos


