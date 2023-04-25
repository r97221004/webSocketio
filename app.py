from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, disconnect
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
@sio_jwt_required()
def handle_message(message):
    print(f"Receive mseeage: {message}")
    if message != "User connected!":
        message = message + ' from backend'
        send(message, broadcast=True)


@socketio.on('disconnect.request', namespace='/index')
@sio_jwt_required()
def disconnect_request():
    sid = request.sid
    disconnect(sid)
    print("success!!! sid[{}] disconnect ".format(sid))


@socketio.on('connect', namespace='/demo')
@sio_jwt_required()
def connect():
    sid = request.sid
    print(f'User {sid} connected')


@socketio.on('send', namespace='/demo')
def chat(data):
    socketio.emit('get', data, namespace='/demo')


@socketio.on('test', namespace='/demo')
def test():
    socketio.send("test", namespace='/demo')


@app.route("/demo")
def demo1():
    return render_template("demo.html")


@app.route('/index')
def test():
    return render_template('index.html')


def consumer_task():
    while True:
        print('start function consumer_task()')
        socketio.sleep(10)

        data = {
            'message': "test function consumser_task()"
        }
        socketio.emit('reply', data, namespace='/demo')


def setup_app():
    socketio.start_background_task(consumer_task)


setup_app()

# if __name__ == "__main__":
#     socketio.run(app, host="192.168.195.128")
