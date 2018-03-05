from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import time
import RPi.GPIO as GPIO
from math import *

leftTriggerPin = 17
leftPwmPin = 27
pwmFrequency = 50
maxInputValue = 150
maxDutyCycle = 40
steeringInputThreshold = 105

GPIO.setmode(GPIO.BCM)
GPIO.setup(leftTriggerPin, GPIO.OUT)
GPIO.setup(leftPwmPin, GPIO.OUT)
leftMotor = GPIO.PWM(leftPwmPin, pwmFrequency)

app = Flask(__name__)
socketio = SocketIO(app)

@socketio.on('joystickState')
def handle_my_custom_event(json):
    x = json['x']
    y = json['y']
    print('received: ' + str(x) + ' ' + str(y))
       
    dutyCycle = (sqrt(pow(x,2) + pow(y,2)) * maxDutyCycle)  / maxInputValue

    if abs(x) > steeringInputThreshold: # Turn
        if x > 0: # Turn right
            rightDutyCycle = -dutyCycle
            leftDutyCycle = dutyCycle
        else: # Turn left
            rightDutyCycle = dutyCycle
            leftDutyCycle = -dutyCycle
    else:
        if y < 0: # Forward
            rightDutyCycle = dutyCycle
            leftDutyCycle = dutyCycle
        else: # Backward
            rightDutyCycle = -dutyCycle
            leftDutyCycle = -dutyCycle
    
    print('leftDutyCycle: ' + str(leftDutyCycle))
    print('rightDutyCycle: ' + str(rightDutyCycle))

    # Forward / backward
    if leftDutyCycle > 0:
        GPIO.output(leftTriggerPin, GPIO.HIGH)
    else:
        GPIO.output(leftTriggerPin, GPIO.LOW)

    #if rightDutyCycle > 0:
    #    GPIO.output(rightTriggerPin, GPIO.HIGH)
    #else:
    #    GPIO.output(rightTriggerPin, GPIO.LOW)

    leftMotor.ChangeDutyCycle(dutyCycle)
    # rightMotor.ChangeDutyCycle(dutyCycle)
    
@socketio.on('connect')
def test_connect():
    print('Client connected')
    leftMotor.start(0)

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')
    leftMotor.stop()
    GPIO.cleanup()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8080)
