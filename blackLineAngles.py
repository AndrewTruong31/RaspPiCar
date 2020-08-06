import numpy as np
import cv2
import motorControl as motor
import manualControl as control


def main():
    cap = cv2.VideoCapture(0) #sets the camera 
    cap.set(3,640) #adjusts width of video stream
    cap.set(4,480) #adjusts height of video stream
    cap.set(5,30) #adjusts frame rate of video stream
    motor.setAngle(45)

    while(True): #infinite loop with break condition at bottom
        ret, frame = cap.read() #creates the frame with the camera
        frame = cv2.flip(frame, -1)

        fullCont = findContour(frame) #contour for the entire frame
        c = max(fullCont, key=cv2.contourArea) #finds the largest contour
        x, y, w, h = cv2.boundingRect(c) #returns the coresponding values creating a rect around the contour
        cv2.rectangle(frame, (x,y), ((x+w), (y+h)), (0, 255, 0), 3) #draws a box to bound the contour area

        small_box = cv2.minAreaRect(c)
        (x_min, y_min), (w_min, h_min), ang = small_box

        if(ang < -45):
            ang = 90 + ang
        if(w_min < h_min and ang > 0):
            ang = (90 - ang) * -1
        if(w_min > h_min and ang < 0):
            ang = 90 + ang

        ang = int(ang)
        box = cv2.boxPoints(small_box)
        box = np.int0(box)
        

        if(ang > 0):
            print("turn R", end="\r", flush=True)
        elif(ang < 0 ):
            print("turn L", end="\r", flush=True)


        #draws the angle and the box after the image if fully processed 
        cv2.drawContours(frame, [box], 0, (0, 0, 255), 2) 
        cv2.putText(frame, str(ang) + ' deg', (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
        
        cv2.imshow('frame', frame)

        if cv2.waitKey(20) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def findContour(frame):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #converts the coloured frame into grayscale
    blur_frame = cv2.GaussianBlur(gray_frame,(5,5),0) 
    ret, thresh = cv2.threshold(blur_frame, 50, 255, cv2.THRESH_BINARY_INV) #removes all non-black objects from frame
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) #finds all of the contours on the frame
    return contours

if __name__ == '__main__':
    main()