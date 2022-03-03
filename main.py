import time,sys
import RPi.GPIO as GPIO
import asyncio
import websockets
import socket

in3 = 23
in4 = 24
in1 = 22
in2 = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)

direction=''

def turn_left():
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.HIGH)
    GPIO.output(in4,GPIO.LOW)
    GPIO.output(in3,GPIO.HIGH)

def turn_right():
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.HIGH)
def move_forward():
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in4,GPIO.LOW)
    GPIO.output(in3,GPIO.HIGH)

def move_backward():
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.HIGH)
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.HIGH)

def stop():
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.LOW)
turn_right()
time.sleep(2)
turn_left()
time.sleep(2)
stop()
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


hostname = socket.gethostname()
IPAddr = get_ip()
print("Your Computer Name is: " + hostname)
print("Your Computer IP Address is: " + IPAddr)

async def echo(websocket, path):
    async for message in websocket:
        if path == '//gyroscope':
            data = await websocket.recv()
            print(data)
        if path == '//orientation':
            data = await websocket.recv()
            l=data.split(',')
            x=int(float(l[-1]))
            y=int(float(l[-2]))
            if(y>20 and y<50):
                turn_right()
                print("right")
            elif(y>310 and y<345):
                turn_left()
                print("left")
            elif(x>310 and x<360):
                move_forward()
                print("forward")
            elif(x<240 and x>190):
                move_backward()
                print("backward")
            else:
                stop()
try:
    asyncio.get_event_loop().run_until_complete(websockets.serve(echo, '0.0.0.0', 5000))
    asyncio.get_event_loop().run_forever()
except KeyboardInterrupt:
    GPIO.cleanup()
    stop()