var Gpio = require('pigpio').Gpio
var io = require('socket.io')(http);

led = new Gpio(17, {mode: Gpio.OUTPUT});

io.on('connection', function (socket) {
    socket.broadcast.emit('hi');
    console.log('a user connected');
    socket.on('disconnect', function () {
        console.log('user disconnected');
    });
    socket.on('joystickState', function (msg) {
        console.log('joystickState: ' + msg.x + ' ' + msg.y);
        led.pwmWrite(Math.abs(msg.x | 0));
    });
});