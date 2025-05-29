from flask import Blueprint, render_template, request, redirect, url_for,session,flash
from db import salvar_projeto, buscar_projeto, excluir_projeto, buscar_projeto_por_id, atualizar_projeto

projeto_route = Blueprint('projeto_route', __name__)


@projeto_route.route('/projeto', methods=['GET', 'POST'])
def listar_projetos():
    if request.method == 'POST': 
        nome = request.form['nome']
        descricao = request.form['descricao']
        data_inicio = request.form['data_inicio']
        data_fim = request.form['data_fim']
        responsavel = request.form['responsavel']  
        equipe = request.form['equipe']  

        salvar_projeto(nome, descricao, data_inicio, data_fim, responsavel, equipe)
        return redirect(url_for('projeto_route.listar_projetos'))  

    projeto = buscar_projeto() 
    return render_template('projeto.html', projetos=projeto)  

 

@projeto_route.route('/excluir/<int:id>', methods=['POST'])
def excluir_projeto_route(id):
    if session.get('perfil') not in ['admin', 'gestor']:
        return redirect(url_for('projeto_route.listar_projetos'))

    excluir_projeto(id)
    flash("Projeto excluído com sucesso.")
    return redirect(url_for('projeto_route.listar_projetos'))



@projeto_route.route('/projeto/editar/<int:id>', methods=['GET', 'POST'])
def editar_projeto(id):
    if session.get('perfil') not in ['admin', 'gestor']:
        return redirect(url_for('projeto_route.listar_projetos'))
    
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        data_inicio = request.form['data_inicio']
        data_fim = request.form['data_fim']
        responsavel = request.form['responsavel']  
        equipe = request.form['equipe']  

        atualizar_projeto(id, nome, descricao, data_inicio, data_fim, responsavel, equipe)
        return redirect(url_for('projeto_route.listar_projetos'))  

    projeto = buscar_projeto_por_id(id)  
    return render_template('projeto.html', projeto_editar=projeto, projetos=buscar_projeto())  

