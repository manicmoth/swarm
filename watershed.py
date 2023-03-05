import cv2 as cv
from numpy import ones, uint8
# using distance transform with a watershed algorithm to produce segmented images
# Given an image (edited or not) identify objects from background, then identify borders
# this function will be used with the selection tool.


class WatershedSegmenter():

    def __init__(self, im)-> None:
        """
        Initializes watershed segmenter, performs initial calculations to produce 
        a sure bg and fg from an image.
        
        im - cv image of size (n,m,3)
        """
        
        self.img = im
        self.gray = cv.cvtColor(self.img,cv.COLOR_BGR2GRAY)
        self.ret, self.tresh = cv.threshold(self.gray, 0, 255, cv.THRESH_BINARY_INV+cv.THRESH_OTSU)
        
        # noise removal 
        self.kernal = ones((3,3),uint8)
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
        self.sure_fg = uint8(self.sure_fg)
        self.unknown = cv.subtract(self.sure_bg,self.sure_fg)
       

    def segment(self)-> tuple:
        """
        Delinates objects in foreground from background, giving an image with 
        color values mapping this deliniation, also gives an image of only the 
        borders imposed ontop of foreground objects.
        """
        self.ret, self.markers = cv.connectedComponents(self.sure_fg)
        self.markers +=1
        
        self.markers[self.unknown==255]=0
        
        self.markers = cv.watershed(self.img,self.markers)
        self.img[markers == -1] = [255,0,0]
        
        # markers image should be clearly delinated from the background  
        # img should have borders between objects defined 
        return self.img, self.markers




