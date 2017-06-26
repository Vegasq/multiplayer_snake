from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_socketio import send, emit

import os
from messages import NEW_CLIENT, GO_UP, GO_DOWN, GO_RIGHT, GO_LEFT, GET_WORLD, CLIENT_RESET


from networking import Client


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@socketio.on('map')
def handle_message(data):
    cli = Client()
    resp = cli.send(GET_WORLD)
    emit("map", resp)


@socketio.on('key_pressed')
def handle_message(data):
    cli = Client()

    client_uuid, command = data.split("|")
    cli.set_uuid(client_uuid)
    cli.send(NEW_CLIENT)

    if command == "up":
        cli.send(GO_UP)
    elif command == "down":
        cli.send(GO_DOWN)
    elif command == "left":
        cli.send(GO_LEFT)
    elif command == "right":
        cli.send(GO_RIGHT)
    elif command == "r":
        cli.send(NEW_CLIENT)


@app.route('/')
def index():
    return render_template('client.html')


if __name__ == '__main__':
    socketio.run(app)
