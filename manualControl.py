import motorControl as motor
import time
from pynput import keyboard

def on_release(key):
    try:
        if key.char in ['w', 'a', 's', 'd']:
            motor.stop()
    except:
        k = key.name

def on_press(key):
    angle = motor.getAngle()
    if key == keyboard.Key.esc:
        return False  # stop listener
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys

    if (k == 'w'):
        motor.forward(0.25)
    elif (k == 's'):
        motor.backward(0.25)
    elif (k == 'a'):
        motor.left(0.5)
    elif (k == 'd'):
        motor.right(0.5)
    elif (k == 'up'):
        angle += 2
        if(angle > 120):
            angle = 120
        motor.setAngle(angle)
    elif (k == 'down'):
        angle -= 2
        if(angle < 14):
            angle = 14
        motor.setAngle(angle)

listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()
    


        