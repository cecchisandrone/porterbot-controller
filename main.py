from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import time
import RPi.GPIO as GPIO
from math import *
import signal

def handle_exit_signal(signal_number, stack):
    print("Detected signal " + str(signal_number))
    print('Quitting porterbot-controller')
    leftMotor.stop()
    rightMotor.stop()
    GPIO.cleanup()
    print('Cleanup terminated')
    exit()
    
signal.signal(signal.SIGTERM, handle_exit_signal)
signal.signal(signal.SIGINT, handle_exit_signal)
signal.signal(signal.SIGHUP, handle_exit_signal)

leftForwardPin = 22
leftBackwardPin = 27
leftPwmPin = 17
rightForwardPin = 13
rightBackwardPin = 6
rightPwmPin = 5
pwmFrequency = 3000
maxInputValue = 175
maxDutyCycle = 40
steeringInputThreshold = 105

GPIO.setmode(GPIO.BCM)

# Left pins setup
GPIO.setup(leftForwardPin, GPIO.OUT)
GPIO.setup(leftBackwardPin, GPIO.OUT)
GPIO.setup(leftPwmPin, GPIO.OUT)
leftMotor = GPIO.PWM(leftPwmPin, pwmFrequency)

# Right pins setup
GPIO.setup(rightForwardPin, GPIO.OUT)
GPIO.setup(rightBackwardPin, GPIO.OUT)
GPIO.setup(rightPwmPin, GPIO.OUT)
rightMotor = GPIO.PWM(rightPwmPin, pwmFrequency)

app = Flask(__name__)
socketio = SocketIO(app)
print('porterbot-controller initialization completed')

@socketio.on('joystickState')
def handle_my_custom_event(json):
    x = json['x']
    y = json['y']
    #print('received: ' + str(x) + ' ' + str(y))
       
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
    
    #print('leftDutyCycle: ' + str(leftDutyCycle))
    #print('rightDutyCycle: ' + str(rightDutyCycle))

    # Forward / backward
    if leftDutyCycle > 0:
        GPIO.output(leftForwardPin, GPIO.HIGH)
        GPIO.output(leftBackwardPin, GPIO.LOW)
    else:
        GPIO.output(leftForwardPin, GPIO.LOW)
        GPIO.output(leftBackwardPin, GPIO.HIGH)

    if rightDutyCycle > 0:
        GPIO.output(rightForwardPin, GPIO.HIGH)
        GPIO.output(rightBackwardPin, GPIO.LOW)
    else:
        GPIO.output(rightForwardPin, GPIO.LOW)
        GPIO.output(rightBackwardPin, GPIO.HIGH)

    leftMotor.ChangeDutyCycle(dutyCycle)
    rightMotor.ChangeDutyCycle(dutyCycle)
    
@socketio.on('connect')
def test_connect():
    print('Client connected')
    leftMotor.start(0)
    rightMotor.start(0)

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')
    leftMotor.stop()
    rightMotor.stop()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8080)

