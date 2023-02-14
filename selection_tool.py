import cv2 as cv
import numpy as np
import os
import copy

# Function takes in an image, allows selection of the subject and defining 
# inclusions & exclusions
# currently searches for image at img "image.jpg" and uses it as the canvas 
# @param image input photo 
# @return "savedImage.jpg" image marked up image  
# @return rect_coords nested tuple of coords

# TODO parameterize to accept image thrown at it
#      parameterize image size, to be standard (1080p)

# TODO Refactor code into class

color = True

# example code from https://mlhive.com/2022/04/draw-on-images-using-mouse-in-opencv-python
ix,iy = -1,-1

debug_mode = False  # toggle helpful print statements
drawing = False     # System state variable 
mode = False        # 
file_name = "savedImage.jpg"
path = os.getcwd() + "/img/"
file_name = path  +file_name
colors = [( 0, 0, 0),
          ( 255, 255, 255)]
# read image from path and add callback
img = cv.imread(path + "image.jpg")
#img = np.zeros((512,512,3), np.uint8)
cache = img
rect_coords = ((-1,-1),(-1,-1))

def draw_circle(event,x,y,flags,param):
    global ix,iy,drawing,mode
    global rect_coords 
    global img 
    global cache
     
    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y

    elif event == cv.EVENT_MOUSEMOVE:
        if drawing == True:
            if mode == True:
                pass
                #cv.rectangle(img,(ix,iy),(x,y),(0,255,0),2)
            else:
                if cache.any():
                    img = copy.deepcopy(cache)
                cv.circle(img,(x,y),5,colors[color],-1) 
                cache = copy.deepcopy(img)
                if type(rect_coords) is tuple:
                    cv.rectangle(img,rect_coords[0],rect_coords[1],(0,255,0),1)

    elif event == cv.EVENT_LBUTTONUP:
        drawing = False
        if mode == True: 
            rect_coords = ((x,y),(ix,iy))
            
            if cache.any():
                img = copy.deepcopy(cache)
            else:
                print("WTC _ rect")
                cache = copy.deepcopy(img)
           
            cv.rectangle(img,(ix,iy),(x,y),(0,255,0),1)
            
            if debug_mode:
                print(f"RECTANGLE:\t({ix},{iy})\n \t\t({x},{y})")
        else:
            cv.circle(img,(x,y),5,colors[color],-1)
    
if debug_mode:
    print(file_name)
cv.namedWindow('image')
c = cv.setMouseCallback('image',draw_circle)

while(1):
    cv.imshow('image',img)
    k = cv.waitKey(1) & 0xFF
    #print(f"{ix}{iy}")
    if k == ord('m'):
        mode = not mode
    elif k == ord('c'):
        color = not color
    elif k == 27:
        break
  
cv.imwrite( file_name, cache)

print("image saved")
cv.destroyAllWindows()
print(rect_coords)

