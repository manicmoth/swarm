# grabcut class
import numpy as np
import cv2 as cv
from os import getcwd

class GrabCutSegmenter():

    def __init__(self) -> None:
        """
        Initializes segmenter, and performs first pass of grabcut segmentation 
        using a bounding box
        """
        # define vars
        self.bgdModel = np.zeros((1,65),np.float64) 
        self.fgdModel = np.zeros((1,65),np.float64) 


    def rect_segment(self, im,rec_coords:tuple = ()):
        """
        Performs first pass of grabCut segmentation using a bounding box, gives
        insight to how grabCut will process image 
        
        @param im - cv image of size (3,n,m)
        @param rec_coords tuple of two xy-coordinate pairs that define the 
        the bounding box
        
        @return img - masked image size (n,m,3)
        """
        
        if not isinstance(im, np.ndarray):
            raise Exception("Please pass an img to the segmenter") 
        # self.img is reserved for output image
        if rec_coords == ():
            raise Exception("Please define a bounding rectangle")
        
        mask = np.zeros(im.shape[:2], np.uint8)

        bounding_coords = rec_coords
        new_mask, _, _ = cv.grabCut(im, mask, bounding_coords, self.bgdModel,self.fgdModel,5,cv.GC_INIT_WITH_RECT)
        output_mask = np.where((new_mask==2)|(new_mask==9),0,1).astype('uint8')
        output_im = im*output_mask[:,:,np.newaxis]

        return output_mask, output_im

    def mask_segment(self,im, mask):
        '''
        Creates an updated mask of an object using grabCut segmentation and a 
        user defined mask. Assumes using the same image as rect_segment.

        @param im - cv image of size (3,n,m)
        @param mask - cv image of size (n,m,3)
        '''
        if not isinstance(im, np.ndarray):
            raise Exception("Please pass an img to the segmenter") 
        # toggle mask where there is black/white
        self.mask[mask == 255] = 1
    
        new_mask, _, _ = cv.grabCut(im,mask,None,self.bgdModel,self.fgdModel,5,cv.GC_INIT_WITH_MASK)
        output_mask = np.where((new_mask==2)|(new_mask==0),0,1).astype('uint8')
        output_im = im*output_mask[:,:,np.newaxis]
        return output_mask, output_im



