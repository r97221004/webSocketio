from flask import Flask, render_template, request
from flask_socketio import SocketIO, send
from auth import sio_jwt_required


app = Flask(__name__)
app.config['SECRET'] = 'secret123'
socketio = SocketIO(app, cors_allowed_origins="*")


@socketio.on('connect', namespace='/index')
@sio_jwt_required()
def connect():
    sid = request.sid
    send(f'sid {sid} connected')


@socketio.on('message', namespace='/index')
def handle_message(message):
    print(f"Receive mseeage: {message}")
    if message != "User connected!":
        message = message + ' from backend'
        send(message, broadcast=True)


# @socketio.on('connect')
# @sio_jwt_required()
# def connect():
#     sid = request.sid
#     send(f'sid {sid} connected')
#     print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ User connected')


# @socketio.on('send')
# def chat(data):
#     socketio.emit('get', data)


# @socketio.on('test')
# def test():
#     socketio.send("test")


# @app.route("/")
# def index():
#     return render_template("index.html")


# @app.route("/demo")
# def demo1():
#     return render_template("demo.html")


@app.route('/test')
def test():
    return render_template('index.html')


if __name__ == "__main__":
    socketio.run(app, host="localhost")
