from detectron_segmenter import Segmenter
from cv2 import imread, imshow, waitKey
from layer import Layer
from layer import Operation

mask_img = imread("/Users/kat/Documents/moth/segmentation_testing/img/gaya.png")
back_img = imread("/Users/kat/Documents/moth/segmentation_testing/img/flowers.jpeg")

segmenter = Segmenter()
masks = segmenter.segment_image(mask_img)

layer = Layer(back_img, masks[0], operation_type=Operation.RESIZE_PADDING)

imshow("out", layer.output_image)
waitKey(0)