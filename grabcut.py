# grabcut class
import numpy as np
import cv2 as cv
from os import getcwd

class GrabCutSegmenter():

    def __init__(self, im, ) -> None:
        """
        Initializes segmenter, and performs first pass of grabcut segmentation 
        using a bounding box
        @param im - cv image of size (3,n,m)
        @param rec_coords tuple of two xy-coordinate pairs that define the 
        the bounding box
        """
        if im == 0:
            raise Exception("Please pass an img to the segmenter")
        
        # self.img is reserved for output image
        self.og_image = im
        # define vars
        self.height, self.width = self.og_image.shape[:2]
        self.mask = np.zeros(self.height, self.width, np.uint8)
        self.bgdModel = np.zeros((1,65),np.float64) 
        self.fgdModel = np.zeros((1,65),np.float64) 
        # perform first grabcut
        print("GrabCutSegmenter: all vars init")

    def rect_segment(self, rec_coords:tuple = ()):
        """
        Performs first pass of grabCut segmentation using a bounding box, gives
        insight to how grabCut will process image 
        
        @return img - masked image size (n,m,3)
        """
        
        if rec_coords == ():
            raise Exception("Please define a bounding rectangle")

        self.bounding_coords = rec_coords
        cv.grabCut(self.og_image, self.mask, self.bounding_coords, 
                   self.bgdModel,self.fgdModel,5,cv.GC_INIT_WITH_RECT)
        self.mask2 = np.where((self.mask==2)|(self.mask==9),0,1).astype('uint8')
        self.img = self.og_image*self.mask2[:,:,np.newaxis]

        print("GrabCutSegmenter: rect_segment complete") 
        return self.img 

    def mask_segment(self, newMask):
        '''
        Creates an updated mask of an object using grabCut segmentation and a 
        user defined mask. Assumes using the same image as rect_segment.
        newMask - cv image of size (n,m,3)
        '''
        # toggle mask where there is black/white
        self.mask[newMask == 255] = 1
        self.mask[newMask == 0] = 0
    
        self.iMask, self.bgdModel,self.fgdModel = cv.grabCut(self.og_image,self.mask,None,self.bgdModel,self.fgdModel,5,cv.GC_INIT_WITH_MASK)
        mask = np.where((self.mask==2)|(self.mask==0),0,1).astype('uint8')
        self.img = self.og_image*mask[:,:,np.newaxis]
        return self.img



