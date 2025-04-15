import sqlite3
import bcrypt


# Função para salvar o usuário
def inserir_usuario(nome, email, senha, perfil):
    senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()
    try:
        cursor.execute(''' 
            INSERT INTO usuarios (nome, email, senha_hash, perfil)
            VALUES (?, ?, ?, ?)
        ''', (nome, email, senha_hash.decode('utf-8'), perfil))
        conn.commit()
        return True, "Usuário cadastrado com sucesso!"
    except sqlite3.IntegrityError:
        return False, "Email já está em uso."
    finally:
        conn.close()

def buscar_usuario_por_email(email):
    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, nome, email, senha_hash, perfil FROM usuarios WHERE email = ?', (email,))
    usuario = cursor.fetchone()
    conn.close()
    return usuario


# Função para salvar o projeto
def salvar_projeto(nome, descricao, data_inicio, data_fim, responsavel, equipe):
    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO projetos (nome, descricao, data_inicio, data_fim, responsavel, equipe)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (nome, descricao, data_inicio, data_fim, responsavel, equipe))
    conn.commit()
    conn.close()

def buscar_projeto():
    conn = sqlite3.connect('banco.db')
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()
    cursor.execute('SELECT id, nome, descricao, data_inicio, data_fim, responsavel, equipe FROM projetos')
    projeto = cursor.fetchall()
    conn.close()
    return projeto

def excluir_projeto(id):
    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM projetos WHERE id = ?', (id,))
    conn.commit()
    conn.close()

def buscar_projeto_por_id(id):
    conn = sqlite3.connect('banco.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT id, nome, descricao, data_inicio, data_fim, responsavel, equipe FROM projetos WHERE id = ?', (id,))
    projeto = cursor.fetchone()
    conn.close()
    return projeto

def atualizar_projeto(id, nome, descricao, data_inicio, data_fim, responsavel, equipe):
    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE projetos
        SET nome = ?, descricao = ?, data_inicio = ?, data_fim = ?, responsavel = ?, equipe = ?
        WHERE id = ?
    ''', (nome, descricao, data_inicio, data_fim, responsavel, equipe, id))
    conn.commit()
    conn.close()

#função tarefa

def buscar_tarefas_por_projeto(projeto_id):
    conn = sqlite3.connect('banco.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''SELECT id, nome, descricao, data_inicio, data_fim, status FROM tarefas WHERE projeto_id = ?''', (projeto_id,))
    tarefas = cursor.fetchall()
    conn.close()
    return tarefas


def salvar_tarefa(nome, descricao, data_inicio, data_fim, projeto_id):
    conn = sqlite3.connect('banco.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tarefas (nome, descricao, data_inicio, data_fim, projeto_id)
        VALUES (?, ?, ?, ?, ?)
    ''', (nome, descricao, data_inicio, data_fim, projeto_id))
    conn.commit()
    conn.close()


def buscar_tarefa_por_id(id):
    conn = sqlite3.connect('banco.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tarefas WHERE id = ?', (id,))
    tarefa = cursor.fetchone()
    conn.close()
    return tarefa

def atualizar_tarefa_no_banco(id, nome, descricao, data_inicio, data_fim):
    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE tarefas
        SET nome = ?, descricao = ?, data_inicio = ?, data_fim = ?
        WHERE id = ?
    ''', (nome, descricao, data_inicio, data_fim, id))
    conn.commit()
    conn.close()

def excluir_tarefa(id):
    conn = sqlite3.connect('banco.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM tarefas WHERE id = ?
    ''', (id,))
    conn.commit()
    conn.close()

