import cv2 as cv
from os import getcwd
# TODO mark these new libraries as dependencies
import laspy as lp
import structuredlight as sl
from fullscreen import FullScreen
import tkinter as tk
import time
from PIL import Image, ImageTk

# Tkinter example code
## example of using opencv array as tkimage:
## https://stackoverflow.com/questions/28670461/read-an-image-with-opencv-and-display-it-with-tkinter

#width  = 640
#height = 480

class SL_Scanner():
    def __init__(self,):
        self.counter = 0        
        self.screen = FullScreen()
        self.width, self.height, self.ch = self.screen.shape
        # genetate structured light frames
        self.gray = sl.Gray() 
        self.imglist = []    
        self.imlist_pattern = self.gray.generate((self.width, self.height))
        self.img_index = []
        self.captures = self.scan(self.screen, self.imlist_pattern)
        self.decode_captures(self.captures)

    def scan(self, scr, il):
        captures = []
        
        cam = cv.VideoCapture(0) # device to capture
        for c,img in enumerate(il):
            scr.imshow(img)
            # TODO take photo, NEEDS TO BE TESTED 
            ret, frame = cam.read()
            cv.imwrite(f"img/c{c}.png",frame)
            time.sleep(.1) 
        cam.release()
        return captures

    def decode_captures(self, caps): 

        img_index = []
        for i in caps:
            img_index.append(self.gray.decode(i, thresh=127))
        
        print(img_index)


if __name__== "__main__":
    app = SL_Scanner()




