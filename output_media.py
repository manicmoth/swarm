from cv2 import imshow, waitKey, resize
from numpy import array
from combinations import ImageCombinations
from copy import deepcopy

class OutputMedia():
    def __init__(self) -> None:
        self.combinations = ImageCombinations()

    def show_vid(self, cap, mask = array([])):
        """
        Displays video with mask over it

        cap- cv2 video capture instance
        mask - mask to display over video

        return - True if video played out, false if user quit
        """
        while(cap.isOpened()):
            ret, frame = cap.read()
            
            ret, frame = cap.read()
            if ret == True:
            # Display the resulting frame
                if len(mask) > 0:
                    frame = self.combinations.apply_mask(frame,mask)
                imshow('Frame', frame)
                # Press Q on keyboard to exit
                if waitKey(25) & 0xFF == ord('q'):
                    return False
        return True
  

    def show_image(self, image, mask = array([])):
        """
        Output masked image

        image - cv2 image
        mask - boolean mask numpy array to apply to img
        """
        if len(mask) > 0:
            image = self._apply_mask(image, mask)
        imshow("output", image)
        waitKey(0)
        pass