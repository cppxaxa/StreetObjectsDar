from threading import Lock
from flask import Flask, render_template, session, request, \
    copy_current_request_context, send_from_directory
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect

async_mode = None

app = Flask(__name__, static_url_path='', static_folder='')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)


@socketio.on('my_ping', namespace='/result')
def ping_pong():
    emit('my_pong')


@socketio.on('connect', namespace='/result')
def test_connect():
    emit('my_response',
         {'data': 'Client connected: ' + request.sid,
          'count': 0})
    print('Client connected', request.sid)
    # emit('my_response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect', namespace='/result')
def test_disconnect():
    emit('my_response',
         {'data': 'Client disconnected: ' + request.sid,
          'count': 0})
    print('Client disconnected', request.sid)


@socketio.on('room_event', namespace='/result')
def send_room_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']},
         room=message['room'])


@socketio.on('join', namespace='/result')
def join(message):
    join_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})


@socketio.on('leave', namespace='/result')
def leave(message):
    leave_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})


plotterProjectDirectory = 'StreetObjectsDarPlotter'
def clientDir(relPath):
    return plotterProjectDirectory + '/' + relPath

@app.route('/models/<path:path>')
def send_models(path):
    return send_from_directory(clientDir('models'), path)

@app.route('/assets/<path:path>')
def send_assets(path):
    return send_from_directory(clientDir('assets'), path)

@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

@app.route('/plot')
def root():
    return app.send_static_file(clientDir('index.html'))


if __name__ == '__main__':
    socketio.run(app, debug=False)
