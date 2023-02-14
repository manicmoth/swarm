from detectron_segmenter import Segmenter
from cv2 import imread, imshow, waitKey

if __name__ == "__main__":
    segmenter = Segmenter()
    im = imread("/Users/kat/Documents/moth/segmentation_testing/imgs/gaya.jpg")
    masks = segmenter.segment_image(im)
    im[masks[0] == 0] = (255,255,255)
    imshow("image",im)
    waitKey(0)