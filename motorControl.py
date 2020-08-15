from gpiozero import Motor
from gpiozero import AngularServo
import time
import pigpio


motorL = Motor(14,15)
motorR = Motor(23,24)
pi = pigpio.pi()

angle = 90

# servo = AngularServo(18, min_angle=0, max_angle=120, min_pulse_width=0.9/1000, max_pulse_width=2.1/1000)

def setAngle(ang):
    global angle
    #angle comes in as 0-120
    if(angle > 120): #safety 
        angle = 120
    if(angle < 32):
        angle = 32
    #pulsewidth is between 900 - 2100 us
    angle = ang
    conv = ((angle/120) * 1200) + 900 # + 900 to account for the min of the pulsewidth
    pi.set_servo_pulsewidth(18, conv)

def tilt(inc):
    global angle
    angle += inc
    setAngle(angle)

def getAngle():
    global angle
    return angle

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

def dynamicForward(speedL, speedR):
    motorL.forward(speedL)
    motorR.forward(speedR)

def dynamicBackward(speedL, speedR):
    motorL.backward(speedL)
    motorR.backward(speedR)

def dynamicLeft(speedL, speedR):
    motorL.backward(speedL)
    motorR.forward(speedR)

def dynamicRight(speedL, speedR):
    motorL.forward(speedL)
    motorR.backward(speedR)

def stop():
    motorL.stop()
    motorR.stop()

def motorVals():
    print(" L: " + str(motorL.value) + "    R: " + str(motorR.value), end="\r", flush=True)
