import motorControl as motor
import time
from pynput import keyboard

angle = 0

def on_press(key):
    global angle
    if key == keyboard.Key.esc:
        return False  # stop listener
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys

    if (k == 'w'):
        motor.forward(1)
    elif (k == 's'):
        motor.backward(1)
    elif (k == 'a'):
        motor.left(1)
    elif (k == 'd'):
        motor.right(1)
    elif (k == 'up'):
        angle += 2
        if(angle > 120):
            angle = 120
        motor.setAngle(angle)
    elif (k == 'down'):
        angle -= 2
        if(angle < 0):
            angle = 0
        motor.setAngle(angle)


listener = keyboard.Listener(
    on_press=on_press)
listener.start()
    


        