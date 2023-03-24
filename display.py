
import cv2 as cv
from os import getcwd
import numpy as np
# TODO mark these new libraries as dependencies
import laspy as lp
import structuredlight as sl
from fullscreen import FullScreen
import tkinter as tk
from screeninfo import get_monitors
from PIL import Image, ImageTk
import time


#    class fullscreen_homebrew(monitor,screen_id:int =select_monitor()):
#        def __init__(self):    
#            width = monitor.width
#            height = monitor.height
#            x = monitor.x
#            y = monitor.y
#            name = str(screen_id)
#
#        cv.namedWindow(name, cv.WINDOW_NORMAL)
#        cv.moveWindow(name, x, y)
#        cv.resizeWindow(name, width, height)
#        cv.setWindowProperty(name, cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
#        img_gray = np.full((height, width), 127, dtype=np.uint8)
#        imshow(img_gray)
#        cv.waitKey(750) 
#
#        def select_monitor():
#            monitors = get_monitors()
#            print("Select the monitor you are projecting with:")
#            for c,m in enumerate(monitors):
#                print(f"{c+1}.\"{str(m.name)}\"\t({m.width}x{m.height})")
#            
#            # take user input here, for now default to non primary
#            other_monitor = 1
#            if len(monitors) == 1:
#                return 0
#            else:
#                return other_monitor
#
class FullScreen_HB:
    """Full-screen with OpenCV High-level GUI backend"""

    delay: int = 1  # internal delay time after imshow

    def __init__(self, screen_id: int = 0):
        self.monitor = get_monitors()[screen_id]
        self.width = self.monitor.width
        self.height = self.monitor.height
        self.x = self.monitor.x
        self.y = self.monitor.y
        self.name = str(screen_id)
        print(self.x, " ",self.y)
        cv.namedWindow(self.name, cv.WINDOW_NORMAL)
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


m = select_monitor()
print(m)

screen = FullScreen_HB(screen_id=m)

width, height, ch = screen.shape 
gray = sl.Gray() 
imglist = []    
imlist_pattern = gray.generate((width, height))
print(width, " ",height)
print(type(imlist_pattern), len(imlist_pattern))
#    print(f"{type(imlist_pattern[0])}")
#    for c,v in enumerate(imlist_pattern):
#        imglist.append(ImageTk.PhotoImage(Image.fromarray(v)))
#        print(f"image {c} converted")



for img in imlist_pattern:
    screen.imshow(img)
    time.sleep(1)
    
screen.destroyWindow()




