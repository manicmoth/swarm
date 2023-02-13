# this program will select all objects of interest as marked by the user.
# using black marks to indicate areas to be removed and white areas for areas to focus.
# This tool is to be used with the selection tool
import numpy as np
import cv2 

def grabcut(input_img, rect):
    """ 
    Takes an image and bounding box and returns a segmented image 

    input_img - cv2 img 
    rect - cv2 rect

    returns - cv2 img
    """
    mask = np.zeros(input_img.shape[:2],np.uint8)

    bgdModel = np.zeros((1,65),np.float64)
    fgdModel = np.zeros((1,65),np.float64)

    rect = (50,50,450,290)
    cv2.grabCut(input_img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)

    mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
    output_img = input_img*mask2[:,:,np.newaxis]

    return output_img