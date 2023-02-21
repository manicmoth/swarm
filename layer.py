


class Image_Layer():
    def __init__(self, image, mask, application_type="resize") -> None:
        """
        image - cv2 image to be masked
        mask - binary array to apply to image
        """
        self.image = image
        self.mask = mask
        self.application_type = application_type