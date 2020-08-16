import numpy as np
import cv2
import manualControl as control
import motorControl as motor
import time

def main():
    face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
    # profileface_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_profileface.xml')
    test_cascade = cv2.CascadeClassifier('cascades/data/aGest.xml')
    cap = cv2.VideoCapture(0)
    cap.set(3,640) #adjusts width of video stream
    cap.set(4,480) #adjusts height of video stream
    cap.set(5,15) #adjusts frame rate of video stream
    motor.setAngle(90)

    while(True):
        ret, frame = cap.read()
        frame = cv2.flip(frame, -1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=3)

        # if(len(faces) <= 0):
        #     faces = profileface_cascade.detectMultiScale(cv2.flip(gray, 1) ,scaleFactor=1.5, minNeighbors=5)
        #     if(len(faces) > 0):
        #         faces[0] = 640 - faces[0]
            
        # if(len(faces) <= 0):
        #     faces = profileface_cascade.detectMultiScale(gray ,scaleFactor=1.5, minNeighbors=5)

        if(len(faces) <= 0): #safety
            motor.stop()

        for(x, y, w, h) in faces:
            # print(x,y,w,h)

            #roi
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]

            color = (255, 0, 0)
            stroke = 2
            end_cord_x = x + w
            end_cord_y = y + h
            cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)

            checkTilt = tilt(frame, x, y, w, h)
            checkPan = pan(frame, x, y, w, h)
            if(checkTilt and checkPan):
                # print('okay')
                pass
            roi(frame, x, y, w, h)


        cv2.imshow('frame', frame)


        if cv2.waitKey(20) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def roi(frame, x, y, w, h):
    #note: frame is 640 x 480
    cx = x + int(w/2) #center x of face
    cy = y + int(h/2) #center y of face

    cv2.circle(frame, (cx,cy), 2, (0,0,255), 2)
    cv2.line(frame, (0, 200), (640, 200), (0, 0, 255), 1)
    cv2.line(frame, (0, 280), (640, 280), (0, 0, 255), 1)

    cv2.line(frame, (0, 100), (640, 100), (0, 0, 150), 1)
    cv2.line(frame, (0, 380), (640, 380), (0, 0, 150), 1)

    cv2.line(frame, (300, 0), (300, 480), (0, 0, 255), 1)
    cv2.line(frame, (380, 0), (380, 480), (0, 0, 255), 1)

    cv2.line(frame, (200, 0), (200, 480), (0, 0, 150), 1)
    cv2.line(frame, (480, 0), (480, 480), (0, 0, 150), 1)



def tilt(frame, x, y, w, h):
    #note: frame is 640 x 480
    cx = x + int(w/2) #center x of face
    cy = y + int(h/2) #center y of face
    # print(cx, cy)
    printTilt(frame, motor.getAngle())
    if(cy > 100 and cy < 380):
        if(cy < 200):
            motor.tilt(1)    
        elif(cy > 280):
            motor.tilt(-1)
        else:
            return True
    else:
        if(cy < 100):
            motor.tilt(4)
        elif(cy > 380):
            motor.tilt(-4)

    return False

def pan(frame, x, y, w, h):
    #note: frame is 640 x 480
    cx = x + int(w/2) #center x of face
    cy = y + int(h/2) #center y of face
    speedS = 0.5
    speedL = 0.75
    if(cx > 200 and cx < 480):
        if(cx < 300):
            # print('left s')
            motor.left(speedS)
        elif(cx > 380):
            # print('right s')
            motor.right(speedS)
        else:
            motor.stop()
            return True
    else:
        if(cx < 200):
            # print('left L')
            motor.left(speedL)
        elif(cx > 480):
            # print('right L')
            motor.right(speedL)
    
    
    return False

def printTilt(frame, ang):
    cv2.putText(frame, str(ang) + ' deg', (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

if __name__ == '__main__':
    main()