import cv2 as cv
import numpy as np

# using distance transform with a watershed algorithm to produce segmented images
# Given an image (edited or not) identify objects from background, then identify borders
# this function will be used with the selection tool.


class WatershedSegmenter():

    def __init__(self, im)-> None:
        """
        Initializes segmenter, performing initial calculations to produce 
        a sure bg and fg from an image
        """
        
        self.img = im
        self.gray = cv.cvtColor(self.img,cv.COLOR_BGR2GRAY)
        self.ret, self.tresh = cv.threshold(self.gray, 0, 255, cv.THRESH_BINARY_INV+cv.THRESH_OTSU)
        
        # noise removal 
        self.kernal = np.ones((3,3),np.uint8)
        # TODO: test effect of changing iterations
        self.opening =cv.morphologyEx(self.thresh, cv.MORPH_OPEN, self.kernal, iterations=2)
        
        #sure background area
        # TODO: test effect of changing iterations
        self.sure_bg = cv.dilate(self.opening,self.kernal,iterations=3)
        
        # Finding Unknown region
        self.scalar = .7
        self.dist_transform = cv.distanceTransform(self.opening,cv.DIST_L2,5)
        self.ret, self.sure_fg = cv.threshold(self.dist_transform,
                                              self.scalar*self.dist_transform.max(),255,0)
        self.sure_fg = np.uint8(self.sure_fg)
        self.unknown = cv.subtract(self.sure_bg,self.sure_fg)
       

    def segment(self)-> tuple:
        self.ret, self.markers = cv.connectedComponents(self.sure_fg)
        self.markers +=1
        
        self.markers[self.unknown==255]=0
        
        self.markers = cv.watershed(self.img,self.markers)
        self.img[markers == -1] = [255,0,0]
        
        # markers image should be clearly delinated from the background  
        # img should have borders between objects defined 
        return self.img, self.markers




