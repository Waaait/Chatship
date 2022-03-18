from flask import Flask, render_template, session, url_for, request, redirect
from flask_socketio import SocketIO, join_room, leave_room, emit
from flask_session import Session

app = Flask(__name__)
app.Debug = True
app.config['SECRET_KEY'] = 'secret'
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
        #Store the data
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
    room = session.get('room')
    join_room(room)
    emit('status', {'msg' : session.get('username') + ' has entered the space.'}, room=room)

@socketio.on('text', namespace='/chatroom')
def on_join(data):
    room = session.get('room')
    join_room(room)
    emit('message', {'msg' : session.get('username') + ': '+data['msg']}, room=room)

@socketio.on('leave', namespace='/chatroom')
def on_leave(data):
    username = session.get('username')
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg' : session.get('username') + ' has left the room.'}, room=room)
    session.clear()

if __name__=='__main__':
    socketio.run(app)