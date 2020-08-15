import numpy as np
import cv2
import manualControl as control
import motorControl as motor

def main():
    face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
    profileface_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_profileface.xml')
    cap = cv2.VideoCapture(0)
    motor.setAngle(90)

    while(True):
        ret, frame = cap.read()
        frame = cv2.flip(frame, -1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)

        if(len(faces) <= 0):
            faces = profileface_cascade.detectMultiScale(cv2.flip(gray, 1) ,scaleFactor=1.5, minNeighbors=5)
        if(len(faces) <= 0):
            faces = profileface_cascade.detectMultiScale(gray ,scaleFactor=1.5, minNeighbors=5)

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

    if(cy > 100 and cy < 380):
        if(cy < 200):
            motor.tilt(1)
        elif(cy > 280):
            motor.tilt(-1)
        else:
            return True
    else:
        if(cy < 100):
            motor.tilt(2)
        elif(cy > 380):
            motor.tilt(-2)

    return False

def pan(frame, x, y, w, h):
    #note: frame is 640 x 480
    cx = x + int(w/2) #center x of face
    cy = y + int(h/2) #center y of face

    if(cx > 200 and cx < 480):
        if(cx < 300):
            # print('left s')
            pass
        elif(cx > 380):
            # print('right s')
            pass
        else:
            return True
    else:
        if(cx < 200):
            # print('left L')
            pass
        elif(cx > 480):
            # print('right L')
            pass
    
    return False


if __name__ == '__main__':
    main()