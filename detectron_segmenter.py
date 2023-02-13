# import some common detectron2 utilities
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog

class Segmenter():
    def __init__(self) -> None:
        self.cfg = get_cfg()
        self.cfg.MODEL.DEVICE = "cpu" ## mps or cuda depending on machine type

        self.cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")) # alternative model "COCO-PanopticSegmentation/panoptic_fpn_R_50_1x.yaml")
        self.cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5  # set threshold for this model
        self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml") 
        self.predictor = DefaultPredictor(self.cfg)

    def segment_image(self,im):
        """
        Finds instances of objects in given image and creates masks of each object 

        im - cv image of size (3,n,m)
        returns - a list of masks of size (n,m) of each detected object
        """
        outputs = self.predictor(im)

        v = Visualizer(im[:, :, ::-1], MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]), scale=1.2)
        out = v.draw_instance_predictions(outputs["instances"].to("cpu"))
        masks = [mask.numpy() for mask in outputs["instances"].to("cpu").pred_masks]
        return masks




