import cv2 as cv
import numpy as np
import os

# Function takes in an image, allows selection of the subject and defining 
# inclusions & exclusions

# @param image input photo 
# @return image marked up image  
# @return coords

# example code from https://mlhive.com/2022/04/draw-on-images-using-mouse-in-opencv-python
ix,iy,sx,sy = -1,-1,-1,-1

points_ = []
circles = False
debug_mode = True


file_name = "savedImage.jpg"
path = os.getcwd() + "/test_images/"
file_name = path  +file_name

# mouse callback function
def draw_lines(event, x, y, flags, param):
    global ix,iy,sx,sy
    global points_
    # if the left mouse button was clicked, record the starting
    if event == cv.EVENT_LBUTTONDOWN:

        # draw circle of 2px
        cv.circle(img, (x, y), 3, (0, 0, 127), -1)

        if ix != -1: # if ix and iy are not first points, then draw a line
            cv.line(img, (ix, iy), (x, y), (0, 0, 127), 2, cv.LINE_AA)
        else: # if ix and iy are first points, store as starting points
            sx, sy = x, y
        ix,iy = x, y
        points_.append((x,y))
    elif event == cv.EVENT_LBUTTONDBLCLK:
        ix, iy = -1, -1 # reset ix and iy
        if flags == 33: # if alt key is pressed, create line between start and end points to create polygon
            cv.line(img, (x, y), (sx, sy), (0, 0, 127), 2, cv.LINE_AA)


# mouse callback function
def draw_circle(event,x,y,flags,param):
    global ix,iy,iix,iiy,drawing,mode
    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y
    elif event == cv.EVENT_MOUSEMOVE:
        if drawing == True:
            if mode == True:
                pass
                #cv.rectangle(img,(ix,iy),(x,y),(0,255,0),2)
            else:
                cv.circle(img,(x,y),5,(255,255,255),-1)
    elif event == cv.EVENT_LBUTTONUP:
        drawing = False
        if mode == True:
            cv.rectangle(img,(ix,iy),(x,y),(0,255,0),1)
            iix,iiy = x,y
            if debug_mode:
                print(f"RECTANGLE:\t({ix},{iy})\n \t\t({x},{y})")
            else:
                print(f"{ix}{iy}{x}{y}")

        else:
            cv.circle(img,(x,y),5,(0,0,255),-1)

if debug_mode:
    print(file_name)
# read image from path and add callback
if not circles:
    img = cv.imread(path+"/image.jpg")
    cv.namedWindow('image') 
    c = cv.setMouseCallback('image',draw_lines)
    while(1):
        cv.imshow('image',img)
        if cv.waitKey(20) & 0xFF == 27:
            break
    

else: 
    img = np.zeros((512,512,3), np.uint8)
    cv.namedWindow('image')
    c = cv.setMouseCallback('image',draw_circle)
    
    while(1):
        cv.imshow('image',img)
        k = cv.waitKey(1) & 0xFF
        #print(f"{ix}{iy}")
        if k == ord('m'):
            mode = not mode
        elif k == 27:
            break
  
cv.imwrite( file_name, img)
if circles:
    print(f"{ix},{iy}\t{iix},{iiy}")
print("image saved")
cv.destroyAllWindows()

