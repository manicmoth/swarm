from detectron_segmenter import Segmenter
from output_media import OutputMedia
from cv2 import imread, VideoCapture

if __name__ == "__main__":
    segmenter = Segmenter()
    output = OutputMedia()

    mask_img = imread("/Users/kat/Documents/moth/segmentation_testing/imgs/scout.jpg")
    output_vid = VideoCapture('/Users/kat/Documents/moth/segmentation_testing/imgs/fluid.mp4')
    
    masks = segmenter.segment_image(mask_img)
    
    output.show_vid(output_vid, mask=masks[0])