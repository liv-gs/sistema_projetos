from flask import Flask
from routes import cadastro_route, login_route, inicial_route, projeto_route, tarefa_route, execucao_route



app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  


UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Registra as rotas
app.register_blueprint(cadastro_route)
app.register_blueprint(login_route)
app.register_blueprint(inicial_route)
app.register_blueprint(projeto_route)
app.register_blueprint(tarefa_route)
app.register_blueprint(execucao_route)


if __name__ == '__main__':
    app.run(debug=True)

