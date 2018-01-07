from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
p = GPIO.PWM(17, 2)  # channel=17 frequency=2Hz

app = Flask(__name__)
socketio = SocketIO(app)


@socketio.on('joystickState')
def handle_my_custom_event(json):
    x = json['x']
    y = json['y']
    print('received: ' + str(x) + ' ' + str(y))
    p.ChangeDutyCycle((abs(x) * 100) / 150)
    if y != 0:
        p.ChangeFrequency((abs(y) * 100) / 150)

@socketio.on('connect')
def test_connect():
    print('Client connected')
    p.start(0)

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')
    p.stop()
    GPIO.cleanup()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8080)
