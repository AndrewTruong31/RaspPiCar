import numpy as np
import cv2
import lineFollow as follow

def main():
    cap = cv2.VideoCapture(0) #sets the camera 
    cap.set(3,640) #adjusts width of video stream
    cap.set(4,480) #adjusts height of video stream
    cap.set(5,30) #adjusts frame rate of video stream

    while(True): #infinite loop with break condition at bottom
        ret, frame = cap.read() #creates the frame with the camera

        #variables
        crop_frame = []
        cnt = []
        center = []

        #segments the framme into 4 slices (4 segments horizontally from the top)
        for i in range (4): 
            crop_frame.append(frame[(i*120):((i+1)*120), 0:640])
            cnt.append(findContour(crop_frame[i])) #finds the contours of the cropped image
            if(len(cnt[i]) > 0): #if contour is found
                c = max(cnt[i], key=cv2.contourArea) #finds the contour with the largest area
                cv2.drawContours(crop_frame[i], cnt[i], -1, (0,255,0), 4) #draws the largest contour on the frame
                center.append(drawCenter(c, crop_frame[i])) #stores the center point of each segment to be processed



        cv2.line(frame, (320, 0), (320, 480), (0, 0, 255),2) #draws a red line down the center of the frame 
        cv2.imshow('frame', frame) #displays the frame


        

        print(center[0])


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

def drawCenter(c, frame):
    x, y, w, h = cv2.boundingRect(c) #returns the coresponding values creating a rect around the contour
    M = cv2.moments(c)
    if( M["m00"] != 0):
        cx = int(M['m10']/M['m00']) #calculates the center X point of the contour
        cy = int(M['m01']/M['m00']) #calculates the center Y point of the contour
        cv2.circle(frame, (cx,cy), 5, (255,0,0), 2) #draws a circle at the center points
        cv2.putText(frame, str(abs(320-cx)), (cx,cy+20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1) #displays the distance away from the center (in pixels relative to the res)
        return cx, cy
    else:
        return 0, 0


if __name__ == '__main__':
    main()