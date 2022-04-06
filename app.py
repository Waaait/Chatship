####
#   Main reference: https://github.com/msindev/Chat-App-Flask-SocketIO
###

from flask import Flask, render_template, session, url_for, request, redirect
from flask_socketio import SocketIO, join_room, leave_room, emit
from flask_session import Session

app = Flask(__name__)
app.Debug = True
app.config['SECRET_KEY'] = 'secrete'
app.config['SESSION_TYPE'] = 'filesystem'

Session(app)
socketio = SocketIO(app, manage_session=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/chatroom', methods=['GET', 'POST'])
def chatroom():
    if(request.method=='POST'):
        username = request.form['username']
        room = request.form['room']
        session['username'] = username
        session['room'] = room
        return render_template('chatroom.html', session = session)
    else:
        if(session.get('username') is not None):
            return render_template('chatroom.html', session = session)
        else:
            return redirect(url_for('index'))

@socketio.on('join', namespace='/chatroom')
def on_join(data):
    username = session.get('username')
    room = session.get('room')
    join_room(room)
    emit('status', {'msg' : username + ' has entered '+ room +'.'}, room=room)

@socketio.on('text', namespace='/chatroom')
def text(data):
    username = session.get('username')
    room = session.get('room')
    join_room(room)
    emit('message', {'msg' : username + ': '+data['msg']}, room=room)

@socketio.on('leave', namespace='/chatroom')
def on_leave(data):
    username = session.get('username')
    room = session.get('room')
    leave_room(room)
    session.clear()
    emit('status', {'msg' : username + ' has left '+ room +'.'}, room=room)

if __name__=='__main__':
    socketio.run(app)