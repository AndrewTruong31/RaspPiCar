import numpy as np
import cv2
import motorControl as motor
import manualControl as control
import math


def main():
    cap = cv2.VideoCapture(0) #sets the camera 
    cap.set(3,640) #adjusts width of video stream
    cap.set(4,480) #adjusts height of video stream
    cap.set(5,30) #adjusts frame rate of video stream
    motor.setAngle(40)

    while(True): #infinite loop with break condition at bottom
        ret, frame = cap.read() #creates the frame with the camera
        frame = cv2.flip(frame, -1)

        last = 0

        fullCont = findContour(frame) #contour for the entire frame
        if(len(fullCont) > 0):
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
        
            last = calcSteer(ang)
            
            #draws the angle and the box after the image if fully processed 
            cv2.drawContours(frame, [box], 0, (0, 0, 255), 2) 
            cv2.putText(frame, str(ang) + ' deg', (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
        else:
            if(last == 1):
                motor.right(0.5)
            elif(last == -1):
                motor.left(0.5)
            else:
                motor.stop()
        
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

def calcSteer(ang): #uses algorithm to figure out how much power should be inputted into steering
    
    dyn = math.sqrt(abs(ang)*0.5) #calculation to find how much power should be added to a side
    dyn /= 6.7 #gets the number to be between 0-1

    add = dyn * 0.75 #ensures the number wont exceed 0.25 + num (0-0.75)
    add += 0.25
    add = round(add, 2)
    dyn = round(dyn, 2)

    # add *= 0.5 #temp reduce turning speed

    if(ang > 10):
        motor.dynamicRight(add, add)
        print("turn R: " + str(add), end="\r", flush=True)
        return 1
    elif(ang < -10):
        motor.dynamicLeft(add, add)
        print("turn L: " + str(add), end="\r", flush=True)
        return -1
    else:
        motor.dynamicForward(0.15, 0.15)
        return 0
    #todo make algorithm turn faster the > the ang is from 0, something along the lines of speed += (sqrt(abs(ang)/2)) note: this can exceed 1, need to do more algorithm working 


   

if __name__ == '__main__':
    main()