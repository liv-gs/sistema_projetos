from flask import Blueprint, render_template, request, redirect, url_for, abort
from db import buscar_projeto_por_id, buscar_tarefas_por_projeto, salvar_tarefa, buscar_tarefa_por_id, excluir_tarefa, exc_atualizar_tarefa


tarefa_route = Blueprint('tarefa_route', __name__)
projeto_route = Blueprint('projeto_route', __name__)


@tarefa_route.route('/projeto/<int:projeto_id>/tarefas')
def tarefas_do_projeto(projeto_id):
    projeto = buscar_projeto_por_id(projeto_id)
    tarefas = buscar_tarefas_por_projeto(projeto_id)
    return render_template('tarefas.html', projeto=projeto, tarefas=tarefas)

@tarefa_route.route('/projeto/<int:projeto_id>/tarefas/criar', methods=['POST'])
def salvar_tarefa_route(projeto_id):
    nome = request.form['nome']
    descricao = request.form['descricao']
    data_inicio = request.form['data_inicio']
    data_fim = request.form['data_fim']

    salvar_tarefa(nome, descricao, data_inicio, data_fim, projeto_id)
    return redirect(url_for('tarefa_route.tarefas_do_projeto', projeto_id=projeto_id))


@tarefa_route.route('/tarefa/<int:id>/atualizar', methods=['POST'])
def atualizar_tarefa(id):
    nome = request.form['nome']
    descricao = request.form['descricao']
    data_inicio = request.form['data_inicio']
    data_fim = request.form['data_fim']
    
    projeto_id = request.form.get('projeto_id')  
    if not projeto_id:
        return "Erro: projeto_id não foi enviado", 400
    
    exc_atualizar_tarefa(id, nome, descricao, data_inicio, data_fim)
    return redirect(url_for('tarefa_route.tarefas_do_projeto', projeto_id=projeto_id))


@tarefa_route.route('/tarefa/<int:id>/editar', methods=['GET', 'POST'])
def editar_tarefa(id):
    tarefa = buscar_tarefa_por_id(id)

    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        data_inicio = request.form['data_inicio']
        data_fim = request.form['data_fim']
        projeto_id = request.form['projeto_id']  

        exc_atualizar_tarefa(id, nome, descricao, data_inicio, data_fim)
        return redirect(url_for('tarefa_route.tarefas_do_projeto', projeto_id=projeto_id))


    projeto = buscar_projeto_por_id(tarefa['projeto_id'])
    tarefas = buscar_tarefas_por_projeto(tarefa['projeto_id'])
    return render_template('tarefas.html', tarefa=tarefa, projeto=projeto, tarefas=tarefas)


@tarefa_route.route('/tarefa/<int:id>/excluir', methods=['POST'])
def excluir_tarefa_route(id):
    tarefa = buscar_tarefa_por_id(id)
    if tarefa is None:
        abort(404)

    projeto_id = tarefa['projeto_id']
    excluir_tarefa(id)
    return redirect(url_for('tarefa_route.tarefas_do_projeto', projeto_id=projeto_id))
