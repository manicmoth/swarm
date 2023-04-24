from enum import Enum
import cv2
from helper_functions import apply_mask, Operation


class LayerType(Enum):
    VIDEO = 0
    IMAGE = 1
    

class Layer():
    def __init__(self, base_video=None, base_image=None, mask_image=None, operation_type=Operation.RESIZE_PADDING, name = None) -> None:
        """
        image - cv2 image to be masked
        mask - binary array to apply to image
        operation_type - how the image is related to the mask - see Operation for possible types
        """
        self.operation_type = operation_type

        #check layer type
        if base_video is not None:
            self.base_video = base_video
            _, frame = base_video.read()
            self.base_video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.base_image = frame
            self.layer_type = LayerType.VIDEO
        elif base_image is not None:
            self.base_image = base_image
            self.base_video = None
            self.layer_type = LayerType.IMAGE
        else:
            self.base_image = None
            self.base_video = None
            self.layer_type = LayerType.IMAGE

        #set mask, convert to 1 channel image if necessary
        if not(mask_image is None):
            if len(mask_image.shape) == 3:
                self.mask_image = cv2.cvtColor(mask_image, cv2.COLOR_BGR2GRAY)
            else:
                self.mask_image = mask_image
        else:
            self.mask_image = None

        #apply mask if possible
        if not(self.base_image is None) and not(self.mask_image is None):
            self.output_image = apply_mask(self.mask_image, self.base_image, self.operation_type)
        else:
            self.output_image = None
   
        #set layer name
        if name:
            self.name = name
        else:
            self.name = None

    def get_masked_img(self):
        """
        Returns image with mask applied as defined by operation type
        """
        if self.output_image is None:
            if self.base_image is None:
                return None
            else:
                return self.base_image
        return self.output_image
    

    def update_image(self, new_img):
        """
        Get new image and apply mask if available
        """
        self.base_image = new_img
        if not(self.mask_image is None):
            self.output_image = apply_mask(self.mask_image, self.base_image, self.operation_type)


    def update_video(self, new_vid):
        """
        Get new image and apply mask if available
        """
        self.base_video = new_vid
        _, frame = self.base_video.read()
        self.base_image = frame        
        self.base_video.set(cv2.CAP_PROP_POS_FRAMES, 0)


        if not(self.mask_image is None):
            self.output_image = apply_mask(self.mask_image, self.base_image, self.operation_type)


    
    def update_mask(self, new_mask):
        """
        Applies new mask to image
        """
        if len(new_mask.shape) == 3:
            self.mask_image = cv2.cvtColor(new_mask, cv2.COLOR_BGR2GRAY)
        else:
            self.mask_image = new_mask
        if not(self.base_image is None):
            self.output_image = apply_mask(self.mask_image, self.base_image, self.operation_type)


    def output_video(self):
        """
        Return masked list of frames
        """
        self.base_video.set(cv2.CAP_PROP_POS_FRAMES, 0)
        masked_output_video = []
        while cv2.isOpened(self.output_video):
            _, frame = self.output_video.read()
            output = apply_mask(self.mask_image, frame, self.operation_type)
            masked_output_video.append(output)
        return masked_output_video


    def set_name(self, name):
        self.name = name


