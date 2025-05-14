from flask import Blueprint, render_template, request, redirect, url_for
from db import salvar_execucao, buscar_execucoes, buscar_projetos_por_execucao, buscar_projeto, adicionar_projeto_a_execucao
from flask import flash



execucao_route = Blueprint('execucao_route', __name__)

@execucao_route.route('/execucao', methods=['GET', 'POST'])
def listar_execucoes():
    if request.method == 'POST': 
        nome = request.form['nome']
        descricao = request.form['descricao']
        data_inicio = request.form['data_inicio']
        data_fim = request.form['data_fim']
        
        salvar_execucao(nome, descricao, data_inicio, data_fim)
        return redirect(url_for('execucao_route.listar_execucoes'))  

    execucoes = buscar_execucoes()  
    projetos = buscar_projeto() 
    return render_template('execucao.html', execucoes=execucoes, projetos=projetos)



@execucao_route.route('/execucoes/criar', methods=['POST'])
def criar_execucao():
    nome = request.form['nome']
    descricao = request.form['descricao']
    data_inicio = request.form['data_inicio']
    data_fim = request.form['data_fim']

    salvar_execucao(nome, descricao, data_inicio, data_fim)  
    return redirect(url_for('execucao_route.listar_execucoes'))


@execucao_route.route('/execucao/adicionar_projeto', methods=['POST'])
def adicionar_projeto():
    execucao_id = request.form['execucao_id']
    projeto_id = request.form['projeto_id']

    try:
        adicionar_projeto_a_execucao(execucao_id, projeto_id)
        flash("Projeto adicionado com sucesso!")
    except sqlite3.IntegrityError:
        flash("Projeto já adicionado a esta execução.")
    
    return redirect(url_for('execucao_route.listar_execucoes'))



@execucao_route.route('/execucao/<int:execucao_id>/projetos')
def ver_projetos(execucao_id):
    projetos = buscar_projetos_por_execucao(execucao_id)
    return render_template('ver_projetos.html', projetos=projetos, execucao_id=execucao_id)
