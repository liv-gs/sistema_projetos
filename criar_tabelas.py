import sqlite3

# TABELA USUÁRIOS
def criar_tabela_usuarios():
    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha_hash TEXT NOT NULL,
            perfil TEXT CHECK(perfil IN ('admin', 'gestor', 'colaborador')) NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# TABELA PROJETOS
def criar_tabela_projeto():
    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS projetos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT,
            data_inicio DATE,
            data_fim DATE,
            responsavel TEXT,
            equipe TEXT
        )
    ''')
    conn.commit()
    conn.close()

# TABELA TAREFAS
def criar_tabela_tarefas():
    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            projeto_id INTEGER NOT NULL,
            nome TEXT NOT NULL,
            descricao TEXT,
            data_inicio DATE,
            data_fim DATE,
            status TEXT DEFAULT 'pendente',
            FOREIGN KEY (projeto_id) REFERENCES projetos(id)
        )
    ''')
    conn.commit()
    conn.close()

# Chama as funções para criar as tabelas
if __name__ == '__main__':
    criar_tabela_usuarios()
    criar_tabela_projeto()
    criar_tabela_tarefas()

    print("Tabelas criadas com sucesso!")
