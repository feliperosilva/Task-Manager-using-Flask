# Versões utilizadas
# Python 3.12.2
# Flask 3.0.3
# Werkzeug 3.0.3
# SQLite3 3.41.2

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)  # servidor web Flask
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database/tarefas.db'  # ligação à base de dados pelo SQLAlchemy
# no início
db = SQLAlchemy(app)  # cursor para a base de dados SQLite


class Tarefa(db.Model):
    __tablename__ = "tarefas"
    id = db.Column(db.Integer,
                   primary_key=True)  # ID único (primary_key) necessário para se identificar dentro da base de dados
    conteudo = db.Column(db.String(200))  # Conteúdo da tarefa com valor máximo de 200 caracteres
    concluida = db.Column(db.Boolean)  # Valor booleano que indica se a tarefa foi concluída ou não


with app.app_context():
    db.create_all()  # Criação das tabelas
    db.session.commit()  # Execução das tarefas pendentes na base de dados


@app.route('/')  # a barra conhece-se como página de início, ou home
def home():
    # Nesta variável estão armazenadas todas as tarefas e deve ser entregue ao template index.html
    todas_tarefas = Tarefa.query.all()  # Consultamos e armazenamos todas as tarefas da base de dados
    return render_template("index.html", lista_de_tarefas=todas_tarefas)  # Carrega sempre o template index.hmtl


@app.route('/criar-tarefa', methods=['POST'])
def criar():
    # instância da classe Tarefa
    tarefa = Tarefa(conteudo=request.form['conteudo_tarefa'], concluida=False)  # ID gera-se automaticamente
    db.session.add(tarefa)  # adicionar objeto à base de dados
    db.session.commit()  # Executar a operação pendente
    return redirect(url_for('home'))  # Redireciona para a função home()


@app.route('/tarefa-concluida/<id>')
def concluida(id):
    tarefa = Tarefa.query.filter_by(id=int(id)).first()  # Obtém-se a tarefa procurada
    tarefa.concluida = not tarefa.concluida  # guardar o contrário da variável booleana da tarefa
    db.session.commit()  # Executa a função pendente na base de dados
    return redirect(url_for('home'))  # Redireciona para a função home()


@app.route('/eliminar-tarefa/<id>')
def eliminar(id):
    tarefa = Tarefa.query.filter_by(id=int(id)).delete()  # Pesquisa dentro da base de dados, compara os ids da base
    # de dados e do parâmetro da rota e apaga aquele id
    db.session.commit()
    return redirect(url_for(
        'home'))  # Redireciona à função home() e, se tudo corre bem, aquela tarefa eliminada não irá mais aparecer


if __name__ == '__main__':
    app.run(debug=True)  # debug=True faz com que cada vez que reiniciemos o servidor ou modificamos o código,
    # o Flask reinicia-se sozinho
