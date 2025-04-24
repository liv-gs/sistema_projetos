from flask import Blueprint, render_template, request, redirect, url_for, abort, current_app
from werkzeug.utils import secure_filename
import os
from db import buscar_projeto_por_id, buscar_tarefas_por_projeto, salvar_tarefa, buscar_tarefa_por_id, excluir_tarefa, exc_atualizar_tarefa
from db import get_db_connection

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'docx'}


tarefa_route = Blueprint('tarefa_route', __name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

    arquivo = request.files.get('arquivo')
    arquivo_nome = None  
    arquivo_caminho = None

    if arquivo and allowed_file(arquivo.filename):
        arquivo_nome = secure_filename(arquivo.filename)  
        arquivo_caminho = os.path.join(current_app.config['UPLOAD_FOLDER'], arquivo_nome)
        arquivo.save(arquivo_caminho)
        print(f"Arquivo salvo: {arquivo_nome}")

    salvar_tarefa(nome, descricao, data_inicio, data_fim, projeto_id, arquivo_nome, arquivo_caminho)
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
    
    arquivo = request.files.get('arquivo')
    arquivo_nome = None
    arquivo_caminho = None

    if arquivo and allowed_file(arquivo.filename):
        arquivo_nome = secure_filename(arquivo.filename)
        arquivo_caminho = os.path.join(current_app.config['UPLOAD_FOLDER'], arquivo_nome)
        arquivo.save(arquivo_caminho)

    exc_atualizar_tarefa(id, nome, descricao, data_inicio, data_fim, arquivo_nome, arquivo_caminho)
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

        arquivo = request.files.get('arquivo')
        arquivo_nome = None
        arquivo_caminho = None

        if arquivo and allowed_file(arquivo.filename):
            arquivo_nome = secure_filename(arquivo.filename)
            arquivo_caminho = os.path.join(current_app.config['UPLOAD_FOLDER'], arquivo_nome)
            arquivo.save(arquivo_caminho)

        exc_atualizar_tarefa(id, nome, descricao, data_inicio, data_fim, arquivo_nome, arquivo_caminho)
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

@tarefa_route.route('/upload', methods=['POST'])
def upload_file():
    if 'arquivo' not in request.files:
        return 'Nenhum arquivo enviado'
    
    file = request.files['arquivo']
    
    if file.filename == '':
        return 'Nome de arquivo vazio'
    
    if file:
        upload_folder = current_app.config['UPLOAD_FOLDER']
        filename = secure_filename(file.filename)
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)

        return redirect(url_for('tarefa_route.tarefas_do_projeto', projeto_id=request.form['projeto_id']))
