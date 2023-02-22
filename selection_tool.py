import cv2 as cv
from getopt import getopt
from sys import argv, exit
from os import getcwd
from copy import deepcopy 

# first crack at refactoring selection tool code.
# TODO: implement grabcad and watershed options
# TODO parameterize to accept image thrown at it
#      parameterize image size, to be standard (1080p)

class segmenter():
    def __init__(self,img_name="image.png", img_path=getcwd()+"/img/", output_size=(960,540), output_name="savedImage.jpg"):
        # img_name - name of the image that we will be manipulating
        # Size - tuple of dimensions we will resize our image to
        # Save image name - name for our new image
        # Path - Path to image
        self.color = True
        #example code: https://mlhive.com/2022/04/draw-on-images-using-mouse-in-opencv-python
        self.ix = -1
        self.iy = -1
        self.debug_mode = False  # toggle helpful print statements
        self.drawing = False     # System state variable 
        self.mode = False 
        self.colors = [( 0, 0, 0),
                  ( 255, 255, 255)]
        # read image from path and add callback
        self.file_name = img_name
        self.path = img_path + img_name
        i = cv.imread(self.path)
        self.img = cv.resize(i, output_size)                # Resize image
        #self.img = np.zeros((512,512,3), np.uint8)
        self.cache = self.img
        self.rect_coords = ((-1,-1),(-1,-1))
        self.k = None

    def painter(self,event,x,y,flags,param) -> None:  
        if self.debug_mode:
            print(f"flags {flags} \t event {event}")
        if event == cv.EVENT_LBUTTONDOWN:
            self.drawing = True
            self.ix,self.iy = x,y
            
        elif event == cv.EVENT_MOUSEMOVE:
            if self.drawing == True:
                if self.mode == True:
                    pass
                    #cv.rectangle(img,(ix,iy),(x,y),(0,255,0),2)
                else:
                    if self.cache.any():
                        self.img = deepcopy(self.cache)
                    cv.circle(self.img,(x,y),5,self.colors[self.color],-1) 
                    self.cache = deepcopy(self.img)
                    if type(self.rect_coords) is tuple:
                        cv.rectangle(self.img,self.rect_coords[0],self.rect_coords[1],(0,255,0),1)
            
        elif event == cv.EVENT_LBUTTONUP:
            self.drawing = False
            if self.mode == True: 
                self.rect_coords = ((x,y),(self.ix,self.iy))
                
                if self.cache.any():
                    self.img = deepcopy(self.cache)
                else:
                    print("WTC _ rect")
                    self.cache = deepcopy(self.img)
               
                cv.rectangle(self.img,(self.ix,self.iy),(x,y),(0,255,0),1)
                
                if self.debug_mode:
                    print(f"RECTANGLE:\t({self.ix},{self.iy})\n \t\t({x},{y})")
            else:
                cv.circle(self.img,(x,y),5,self.colors[self.color],-1)

    def run(self):
        # look into using decorators to pass functions to be run at differnet 
        # points, such as which segmenter
        
        if self.debug_mode:
            print(self.file_name)
        cv.namedWindow('Painter')
        cv.setMouseCallback('Painter',self.painter)

        
        while(1):
            print(self.k)
            cv.imshow('Painter',self.img)
            self.k = cv.waitKey(1) & 0xFF
            print(self.k)
            #print(f"{ix}{iy}")
            if self.k == ord('m'):
                # toggling mode between rectangle and paint
                self.mode = not self.mode
            elif self.k == ord('c'):
                # toggling color to be applied to mouse press
                self.color = not self.color
            elif self.k == 27:
                break

def handle_args(argv):
    #img_name, size, save_name, path ):
    opts, args = getopt(argv,"him:s:sn:p",["imgname=","size=","savename=","path="])
    new_defaults = {}
    for opt, arg in opts:
        if opt == '-h':
            print('selection_tool.py -im <imgname> -s <size> -sn <newimgname> -p <path>')
            exit()
        elif opt in ("-im", "--imgname"):
            new_defaults["img_name"]= arg
        elif opt in ("-s", "--size"):
            new_defaults["output_size"] = tuple(eval(arg))
        elif opt in ("-o", "--outputname"):
            new_defaults["output_name"] = arg
        elif opt in ("-p", "--path"):
            new_defaults["img_path"] = arg
    return new_defaults

if __name__ == "__main__":
    manual = segmenter(**handle_args(argv))
    print("Segmenter Initialized")
    # manual.setup(**handle_args(argv))
    manual.run()



