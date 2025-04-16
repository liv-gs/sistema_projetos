from flask import Blueprint, render_template, session, redirect, url_for

inicial_route = Blueprint('inicial_route', __name__)

@inicial_route.route('/inicial')
def inicial():
    if 'usuario_id' not in session:
        return redirect(url_for('login_route.login'))

    nome = session.get('nome')
    perfil = session.get('perfil')  
    return render_template('inicial.html', nome=nome, perfil=perfil)
