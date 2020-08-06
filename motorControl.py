from gpiozero import Motor
from gpiozero import AngularServo
import time
import pigpio


motorL = Motor(14,15)
motorR = Motor(23,24)
pi = pigpio.pi()
# servo = AngularServo(18, min_angle=0, max_angle=120, min_pulse_width=0.9/1000, max_pulse_width=2.1/1000)

def setAngle(angle):
    #angle comes in as 0-120
    conv = ((angle/120) * 1200) + 900
    pi.set_servo_pulsewidth(18, conv) # safe anti-clockwise

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
