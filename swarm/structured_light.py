import cv2 as cv
from os import getcwd
# TODO mark these new libraries as dependencies
import laspy as lp
import structuredlight as sl
from fullscreen import FullScreen
import tkinter as tk
import time
import structuredlight as sl
from screeninfo import get_monitors
import numpy as np

# Tkinter example code
## example of using opencv array as tkimage:
## https://stackoverflow.com/questions/28670461/read-an-image-with-opencv-and-display-it-with-tkinter

#width  = 640
#height = 480

class FullScreen_HB:
    """
    Full-screen with OpenCV High-level GUI backend
    rewriten to work for external projector
    """
    delay: int = 1  # internal delay time after imshow

    def __init__(self, screen_id: int = 0):
        self.monitor = get_monitors()[screen_id]
        self.width = self.monitor.width
        self.height = self.monitor.height
        self.x = self.monitor.x
        self.y = self.monitor.y
        self.name = str(screen_id)
        print(self.x, " ",self.y, self.width," ", self.height)
        
        # had to change this for whatever reason
        cv.namedWindow(self.name)
        cv.moveWindow(self.name, self.x, self.y)
        cv.setWindowProperty(self.name,cv.WND_PROP_FULLSCREEN,cv.WINDOW_NORMAL)
        cv.resizeWindow(self.name, self.width, self.height)
        cv.setWindowProperty(self.name, cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
        
        # set initial image
        img_gray = np.full((self.height, self.width), 127, dtype=np.uint8)
        self.imshow(img_gray)
        cv.waitKey(750)  # first imshow require long delay time

    @property
    def shape(self):
        return self.height, self.width, 3

    def imshow(self, image: np.ndarray):
        cv.imshow(self.name, image)
        cv.waitKey(self.delay)
        cv.waitKey(self.delay)  # magic

    def destroyWindow(self):
        cv.destroyWindow(self.name)


def select_monitor():
    # TODO select camera too -- this is actually an unsolved issue apparently
    monitors = get_monitors()
    print(monitors)
    print("Select the monitor you are projecting with:")
    for c,m in enumerate(monitors):
        print(f"{c}.\"{str(m.name)}\"\t({m.width}x{m.height})")
    
    # take user input here, for now default to non primary
    other_monitor = 1
    if len(monitors) == 1:
        return 0
    else:
        return other_monitor

class SL_Scanner():
    def __init__(self,scr_id):
        self.counter = 0        
        self.screen = FullScreen_HB(screen_id=scr_id)
        self.height, self.width = self.screen.shape[:2]
        # genetate structured light frames
        self.gray = sl.Gray() 
        self.imglist = []    
        self.imlist_pattern = self.gray.generate((self.width, self.height))
        self.img_index = []
        # TODO: separately start scan, pass args for how scan will be performed
        # Scan
        self.captures = self.scan(self.screen, self.imlist_pattern)
        # Decode
        self.decode_captures(self.captures)

    def scan(self, scr, il):
        captures = []
        
        cam = cv.VideoCapture(0) # device to capture
        for c,img in enumerate(il):
            scr.imshow(img)
            # TODO take photo, NEEDS TO BE TESTED 
            ret, frame = cam.read()
            captures.append(frame)
            cv.imwrite(f"img/c{c}.png",frame)
            time.sleep(.1) 
        cam.release()
        return captures

    def decode_captures(self, caps): 

        img_index = []
        for i in caps:
            # look into other decode methods
            img_index.append(self.gray.decode(i, thresh=127))
        
        print(img_index)


if __name__== "__main__":
    app = SL_Scanner(select_monitor())




