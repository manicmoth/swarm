import sys
from os import getcwd

sys_path = getcwd()
sys.path.insert(1, sys_path + "/swarm")

from detectron_segmenter import Segmenter
import cv2
from layer import Layer
from layer import Operation
import numpy as np

projection_area = cv2.imread("/Users/kat/Documents/moth/segmentation_testing/img/gaya.png")
segmenter = Segmenter()
masks = segmenter.segment_image(projection_area)

video = cv2.VideoCapture("/Users/kat/Documents/moth/segmentation_testing/img/testvid.mp4")
layer = Layer(base_video=video, mask_image=masks[0])

new_video = np.array(layer.output_video())
print(new_video.shape)

# output_video = []
# frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)        
# while video.get(cv2.CAP_PROP_POS_FRAMES) < frame_count:
#     _, frame = video.read()
#     output_video.append(frame)


size = new_video[0].shape[0:2]
fourcc = cv2.VideoWriter_fourcc(*'XVID')#VideoWriter_fourcc(*'MP4V')
# out = cv2.VideoWriter("video1.mp4", fourcc, 20.0, size)
out = cv2.VideoWriter('output_video_from_file.avi', cv2.VideoWriter_fourcc('M','J','P','G'), 20, size)

# out = VideoWriter('project.mp4',VideoWriter_fourcc(*'DIVX'), 15, size)
for frame in new_video:
    out.write(frame)
out.release()
print("DONE")
# imshow("out", layer.output_image)
# waitKey(0)