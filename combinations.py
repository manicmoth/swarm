from cv2 import resize

class ImageCombinations():
    """
    Class for image operations
    TODO: include adding images functionality
    """


    def apply_mask(self, img, mask):
        """
        Apply mask to a given image - black out non wanted components

        img - cv2 mat
        mask - boolean mask numpy array to apply to img

        returns - image with mask applied
        """
        #TODO - determine which image to reshape/add padding to, prob an alg for this
        img = resize(img, [mask.shape[1], mask.shape[0]])
        img[mask == 0] = (0,0,0)
        return img
