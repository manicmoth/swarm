import cv2 as cv
import numpy as np
import os

# example code from https://mlhive.com/2022/04/draw-on-images-using-mouse-in-opencv-python
ix,iy,sx,sy = -1,-1,-1,-1

circles = True

# mouse callback function
def draw_lines(event, x, y, flags, param):
    global ix,iy,sx,sy
    # if the left mouse button was clicked, record the starting
    if event == cv.EVENT_LBUTTONDOWN:

        # draw circle of 2px
        cv.circle(img, (x, y), 3, (0, 0, 127), -1)

        if ix != -1: # if ix and iy are not first points, then draw a line
            cv.line(img, (ix, iy), (x, y), (0, 0, 127), 2, cv.LINE_AA)
        else: # if ix and iy are first points, store as starting points
            sx, sy = x, y
        ix,iy = x, y
        
    elif event == cv.EVENT_LBUTTONDBLCLK:
        ix, iy = -1, -1 # reset ix and iy
        if flags == 33: # if alt key is pressed, create line between start and end points to create polygon
            cv.line(img, (x, y), (sx, sy), (0, 0, 127), 2, cv.LINE_AA)


drawing = False # true if mouse is pressed
mode = True # if True, draw rectangle. Press 'm' to toggle to curve
# mouse callback function
def draw_circle(event,x,y,flags,param):
    global ix,iy,drawing,mode
    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y
    elif event == cv.EVENT_MOUSEMOVE:
        if drawing == True:
            if mode == True:
                pass
                #cv.rectangle(img,(ix,iy),(x,y),(0,255,0),2)
            else:
                cv.circle(img,(x,y),5,(0,0,255),-1)
    elif event == cv.EVENT_LBUTTONUP:
        drawing = False
        if mode == True:
            cv.rectangle(img,(ix,iy),(x,y),(0,255,0),1)
            
            print(f"RECTANGLE:\t\t({ix},{iy})\n \t\t\t({x},{y})")
        else:
            cv.circle(img,(x,y),5,(0,0,255),-1)


path = os.getcwd()
# read image from path and add callback
if not circles:
    img = cv.resize(cv.imread(path+"/test_images/image.jpg"), (1280, 720))
    cv.namedWindow('image') 
    cv.setMouseCallback('image',draw_lines)

    while(1):
        cv.imshow('image',img)
        if cv.waitKey(20) & 0xFF == 27:
            break

    cv.destroyAllWindows()

else: 
    img = np.zeros((512,512,3), np.uint8)
    cv.namedWindow('image')
    cv.setMouseCallback('image',draw_circle)
    while(1):
        cv.imshow('image',img)
        k = cv.waitKey(1) & 0xFF
        if k == ord('m'):
            mode = not mode
        elif k == 27:
            break
    cv.destroyAllWindows()

