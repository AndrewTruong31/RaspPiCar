from gpiozero import Motor
import time


motorL = Motor(14,15)
motorR = Motor(23,24)

def forward(speed):
    motorL.forward(speed)
    motorR.forward(speed)

def backward(speed):
    motorL.backward(speed)
    motorR.backward(speed)

def left(speed):
    motorL.backward(speed)
    motorR.forward(speed)

def right(speed):
    motorL.forward(speed) 
    motorR.backward(speed)

def dynamic(speedL, speedR):
    motorL.forward(speedL)
    motorR.forward(speedR)

def stop():
    motorL.stop()
    motorR.stop()

def motorVals():
    print(" L: " + str(motorL.value) + "    R: " + str(motorR.value), end="\r", flush=True)
