from logging import debug
from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, join_room, leave_room, emit, rooms
from flask_session import Session



app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret'
app.config['SESSION_TYPE'] = 'filesystem'
botname = 'robsu'
triagem = 'Triagem'


Session(app)



socketio = SocketIO(app, manage_session=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/chat-admin', methods=['GET', 'POST'])
def admin():
    return render_template('Chat-User.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if(request.method=='POST'):
        username = request.form['username']
        email = request.form['email']
        franquia = request.form['franquia']
        room = request.form['email']
        setor = request.form['setores']


        # room = request.form['room']

        #Store the data in session
        session['username'] = username
        session['email'] = email
        session['franquia'] = franquia
        session['room'] = room
        session['setores'] = setor
        session['botname'] = botname
        session['triagem'] = triagem
        return render_template('Chat-User.html', session = session)
    else:
        if(session.get('username') is not None):
            return render_template('Chat-User.html', session = session)
        else:
            return redirect(url_for('index'))


# quando o usuario loga
@socketio.on('join', namespace='/chat')
def join(message):
    room = session.get('room')
    join_room(room)
    # emit('status', {'msg' : session.get('username') + ' entrou no chat'}, room=room)
    # emit('message', {'msg' : session.get('botname') + ' : olá ' + session.get('username') + ', eu me chamo Robsu, sou o bot de atendimentos da Hausz. Para iniciarmos o seu atendimento atendimento digite "olá robsu"'}, room=room)

# dispara menssagem do usuario
@socketio.on('text', namespace='/chat')
def mensagem_user(message):
    room = session.get('room')
    emit('message', {'msg': message['msg']}, room=room)

# quando usuario sai
@socketio.on('left', namespace='/chat')
def left(message):
    room = session.get('room')
    username = session.get('username')
    leave_room(room)
    session.clear()
    emit('status', {'msg': username + ' saiu do chat.'}, room=room)


if __name__ == '__main__':
    socketio.run(app, debug=True)