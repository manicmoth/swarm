from detectron_segmenter import DetectronSegmenter
from grabcut import GrabCutSegmenter
import numpy as np
import cv2 as cv

class Segmenter():
    """
    Class which handles image segmentation - given an image, returns list of masks
    """

    def __init__(self) -> None:
        self.detectron = DetectronSegmenter()
        self.grabcut = GrabCutSegmenter()

    def auto_segment(self, image: np.ndarray):
        """
        @param image - cv image (numpy array)
        returns - list of binary array masks of segments
        """
        return self.detectron.segment_image(image)
    
    def manual_segment_rect(self, image: np.ndarray, rect: tuple):
        """
        @param image -cv image (numpy array)
        @param rect - tuple of two xy-coordinate pairs that define the bounding box
        returns - segmented cv image mask of image size
        """
        mask, _ = self.grabcut.rect_segment(im=image, rec_coords=rect)
        return [mask]

    def manual_segment_paint(self, image: np.ndarray, mask: np.ndarray):
        """
        @param image - cv image of size (3,n,m)
        @param mask - cv image of size (n,m,3)
        returns - segmented cv image mask of image size
        """
        mask, _ = self.grabcut.mask_segment(im=image, newMask=mask)
        return [mask]