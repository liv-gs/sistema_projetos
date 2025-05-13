import mysql.connector
import bcrypt

#conecção com o banco

def conectar():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='1401',
        database='sistemas',
        
    )

#FUNÇÃO USUÁRIO

def inserir_usuario(nome, email, senha, perfil):
    conn = None  
    try:
        conn = conectar()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        if cursor.fetchone():
            return False, "E-mail já cadastrado."

        cursor.execute(
            "INSERT INTO usuarios (nome, email, senha, perfil) VALUES (%s, %s, %s, %s)",
            (nome, email, senha, perfil)
        )
        conn.commit()
        return True, "Usuário cadastrado com sucesso."

    except mysql.connector.Error as err:
        print("Erro no banco de dados:", err)
        return False, "Erro ao cadastrar usuário."

    finally:
        if conn is not None and conn.is_connected():
            conn.close()


def buscar_usuario_por_email(conn, email):
    conn = conectar()  #fazer a conexão com o banco
    cursor = conn.cursor(dictionary=True) #usado por causa do mariadb com o conector-mysql-python, para retornar dados mais claros
    cursor.execute('SELECT id, nome, email, senha, perfil FROM usuarios WHERE email = %s', (email,)) #buscar no banco com o email informado
    usuario = cursor.fetchone() #retornar do banco uma informação em linha
    cursor.close() #fecha a conexão
    return usuario #retorna 



#FUNÇÃO PROJETO

def salvar_projeto(nome, descricao, data_inicio, data_fim, responsavel, equipe):
    conn = conectar()
    cursor = conn.cursor() #chama o metodo
    cursor.execute('''
        INSERT INTO projetos (nome, descricao, data_inicio, data_fim, responsavel, equipe)
        VALUES (%s, %s, %s, %s, %s, %s)
    ''', (nome, descricao, data_inicio, data_fim, responsavel, equipe))
    conn.commit()
    conn.close()

def buscar_projeto():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)  
    cursor.execute('SELECT id, nome, descricao, data_inicio, data_fim, responsavel, equipe FROM projetos')
    projeto = cursor.fetchall()
    conn.close()
    return projeto

def excluir_projeto(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM projetos WHERE id = %s', (id,))
    conn.commit()
    conn.close()

def buscar_projeto_por_id(id):
    conn = conectar()
    cursor = conn.cursor(dictionary=True) 
    cursor.execute('SELECT id, nome, descricao, data_inicio, data_fim, responsavel, equipe FROM projetos WHERE id = %s', (id,))
    projeto = cursor.fetchone()
    conn.close()
    return projeto

def atualizar_projeto(id, nome, descricao, data_inicio, data_fim, responsavel, equipe):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE projetos
        SET nome = %s, descricao = %s, data_inicio = %s, data_fim = %s, responsavel = %s, equipe = %s
        WHERE id = %s
    ''', (nome, descricao, data_inicio, data_fim, responsavel, equipe, id))
    conn.commit()
    conn.close()






def buscar_tarefas_por_projeto(projeto_id):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT id, nome, descricao, data_inicio, data_fim, arquivo_nome, arquivo_caminho
        FROM tarefas
        WHERE projeto_id = %s
    ''', (projeto_id,))
    tarefas = cursor.fetchall()
    conn.close()
    return tarefas


def salvar_tarefa(nome, descricao, data_inicio, data_fim, projeto_id, arquivo_nome=None, arquivo_caminho=None):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tarefas (nome, descricao, data_inicio, data_fim, projeto_id, arquivo_nome, arquivo_caminho)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    ''', (nome, descricao, data_inicio, data_fim, projeto_id, arquivo_nome, arquivo_caminho))
    conn.commit()
    conn.close()


def buscar_tarefa_por_id(id):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM tarefas WHERE id = %s', (id,))
    tarefa = cursor.fetchone()
    conn.close()
    return tarefa


def exc_atualizar_tarefa(id, nome, descricao, data_inicio, data_fim, arquivo_nome=None, arquivo_caminho=None):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE tarefas
        SET nome = %s, descricao = %s, data_inicio = %s, data_fim = %s, arquivo_nome = %s, arquivo_caminho = %s
        WHERE id = %s
    ''', (nome, descricao, data_inicio, data_fim, arquivo_nome, arquivo_caminho, id))
    conn.commit()
    conn.close()


def excluir_tarefa(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tarefas WHERE id = %s', (id,))
    conn.commit()
    conn.close()


 #FUNÇÃO EXECUÇÕES

def buscar_execucoes():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT id, nome, descricao, data_inicio, data_fim FROM execucoes')
    execucoes = cursor.fetchall()  
    conn.close()
    return execucoes

def salvar_execucao(nome, descricao, data_inicio, data_fim):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO execucoes (nome, descricao, data_inicio, data_fim) 
        VALUES (%s, %s, %s, %s)
    """, (nome, descricao, data_inicio, data_fim))
    conn.commit()  
    conn.close()

def adicionar_projeto_a_execucao(execucao_id, projeto_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO execucoes_projetos (execucao_id, projeto_id) 
        VALUES (%s, %s)
    """, (execucao_id, projeto_id))
    conn.commit()
    conn.close()

def buscar_projetos_por_execucao(execucao_id):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.id, p.nome, p.descricao
        FROM projetos p
        JOIN execucoes_projetos ep ON p.id = ep.projeto_id
        WHERE ep.execucao_id = %s
    """, (execucao_id,))
    projetos = cursor.fetchall()#esera varias linhas de resultado
    conn.close()
    return projetos





