import cv2
from math import ceil, floor
from enum import Enum

class Operation(Enum):
    RESIZE_STRETCH = 0
    RESIZE_PADDING = 1

def apply_mask(mask_image, base_image, operation_type:Operation):
    if operation_type == Operation.RESIZE_STRETCH:
        return resize_stretch()
    elif operation_type == Operation.RESIZE_PADDING:
        return resize_padding()
    else:
        raise Exception("Please Provide Valid Operation Type")


def resize_stretch(mask_image, base_image):
    """
    Shapes image to mask by just resizing 
    """
    output = cv2.resize(base_image, [mask_image.shape[1], mask_image.shape[0]])
    output[mask_image == 0] = (0,0,0)
    return output


def resize_padding(mask_image, base_image):
    """
    Spapes image to mask by smaller dimension and adds padding        
    """
    #height == 0, widht == 1
    mask_width = mask_image.shape[1]
    mask_height = mask_image.shape[0]
    image_width = base_image.shape[1]
    image_height = base_image.shape[0]

    if image_width/image_height < mask_width/mask_height:
        new_height = mask_image.shape[0]
        new_width = base_image.shape[1] * mask_image.shape[0]/base_image.shape[0]
    else:
        new_height = base_image.shape[0] * mask_image.shape[1]/base_image.shape[1]
        new_width = mask_image.shape[1]

    output = cv2.resize(base_image, [int(new_width), int(new_height)])
    height_padding = abs((mask_image.shape[0] - output.shape[0])/2)
    width_padding = abs((mask_image.shape[1] - output.shape[1])/2)

    output = cv2.copyMakeBorder(output, top=floor(height_padding), bottom=ceil(height_padding), left=floor(width_padding), right=ceil(width_padding), borderType=cv2.BORDER_CONSTANT,value=[1,1,1])
    output[mask_image == 0] = (0,0,0)
    return output