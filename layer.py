from enum import Enum
import cv2
from copy import deepcopy
from math import ceil
 
class Operation(Enum):
    RESIZE_STRETCH = 0
    RESIZE_PADDING = 1
    

class Image_Layer():
    def __init__(self, image=None, mask=None, operation_type=Operation.RESIZE_STRETCH, name = None) -> None:
        """
        image - cv2 image to be masked
        mask - binary array to apply to image
        operation_type - how the image is related to the mask - see Operation for possible types
        """
        self.operation_type = operation_type
        self.image = image
        
        self.mask = None
        if not(mask is None):
            self.mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

        if not(image is None) and not(mask is None):
            self.output_image = None
            if self.operation_type == Operation.RESIZE_STRETCH:
                self.output_image = self.resize_stretch()
            elif self.operation_type == Operation.RESIZE_PADDING:
                print("out")
                self.output_image = self.resize_padding()  
   
        if name:
            self.name = name
        else:
            self.name = None

    def resize_stretch(self):
        """
        Shapes image to mask by just resizing 
        """
        output = cv2.resize(self.image, [self.mask.shape[1], self.mask.shape[0]])
        output[self.mask == 0] = (0,0,0)
        return output
    
    def resize_padding(self):
        """
        Spapes image to mask by smaller dimension and adds padding        
        """
        #height/width
        if self.image.shape[0]/self.image.shape[1] > self.mask.shape[0]/self.mask.shape[1]:
             output = cv2.resize(self.image, [int(self.mask.shape[1]*(self.mask.shape[0]/self.image.shape[0])), self.image.shape[0]])

        else:
             output = cv2.resize(self.image, [self.mask.shape[1], int(self.image.shape[0]*(self.mask.shape[1]/self.image.shape[1]))])
        output = cv2.copyMakeBorder(output, (self.mask.shape[0] - output.shape[0])//2, ceil((self.mask.shape[0] - output.shape[0])/2), (self.mask.shape[1] - output.shape[1])//2, ceil((self.mask.shape[1] - output.shape[1])/2), cv2.BORDER_CONSTANT,value=[1,1,1])
        output[self.mask == 0] = (0,0,0)
        return output

    def get_masked_img(self):
        """
        Returns image with mask applied as defined by operation type
        """
        return self.output_image
    
    def update_image(self, new_img):
        """
        Get new image and apply mask if available
        """
        self.image = new_img
        if not(self.mask is None):
            if self.operation_type == Operation.RESIZE_STRETCH:
                self.output_image = self.resize_stretch()
            elif self.operation_type == Operation.RESIZE_PADDING:
                self.output_image = self.resize_padding()

    
    def update_mask(self, new_mask):
        """
        Applies new mask to image
        """
        self.mask = cv2.cvtColor(new_mask, cv2.COLOR_BGR2GRAY)
        if not(self.image is None):
            if self.operation_type == Operation.RESIZE_STRETCH:
                self.output_image = self.resize_stretch()
            elif self.operation_type == Operation.RESIZE_PADDING:
                self.output_image = self.resize_padding()

    def set_name(self, name):
        self.name = name



class Video_Layer():
    def __init__(self, video, mask, operation_type=Operation.RESIZE_STRETCH) -> None:
        """
        image - cv2 image to be masked
        mask - binary array to apply to image
        operation_type - how the image is related to the mask - see Operation for possible types
        """
        self.video = video
        self.mask = mask
        self.operation_type = operation_type   
        self.total_frames = self.video.get(cv2.CAP_PROP_FRAME_COUNT)
     

    def resize_stretch(self, frame):
        """
        Shapes image to mask by just resizing 
        """
        output = cv2.resize(self.image, [self.mask.shape[1], self.mask.shape[0]])
        output[self.mask == 0] = (0,0,0)
        return output
    
    def resize_padding(self, frame):
        """
        Spapes image to mask by smaller dimension and adds padding        
        """
        if frame.shape[0]/self.image.shape[1] > self.mask.shape[0]/self.mask.shape[1]:
             output = cv2.resize(frame, [int(self.mask.shape[1]*(self.mask.shape[0]/frame.shape[0])), frame.shape[0]])

        else:
             output = cv2.resize(frame, [self.mask.shape[1], int(frame.shape[0]*(self.mask.shape[1]/frame.shape[1]))])
        output = cv2.copyMakeBorder(output, (self.mask.shape[0] - output.shape[0])//2, ceil((self.mask.shape[0] - output.shape[0])/2), (self.mask.shape[1] - output.shape[1])//2, ceil((self.mask.shape[1] - output.shape[1])/2), cv2.BORDER_CONSTANT,value=[1,1,1])
        output[self.mask == 0] = (0,0,0)
        return output

    def get_masked_frame_by_index(self, frame_num):
        """
        Returns image with mask applied as defined by operation type
        """
        video_copy = deepcopy(self.video)
        if frame_num >= 0 & frame_num <= self.total_frames:
            # set frame position
            video_copy.set(cv2.CAP_PROP_POS_FRAMES,frame_num)
            ret, frame = video_copy.read()

        output = None
        if self.operation_type == Operation.RESIZE_STRETCH:
            output = self.resize_stretch(frame)
        elif self.operation_type == Operation.RESIZE_PADDING:
            output = self.resize_padding(frame)
        return output
    
    def pop_masked_frame(self):
        """
        Get next frame in video and apply mask
        MODIFIES VIDEO!!!
        """
        ret, frame = self.video.read()
        if self.operation_type == Operation.RESIZE_STRETCH:
            output = self.resize_stretch(frame)
        elif self.operation_type == Operation.RESIZE_PADDING:
            output = self.resize_padding(frame)
        return output
