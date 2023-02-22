import structuredlight as sl
import cv2 as cv
from os import getcwd
# TODO mark these new libraries as dependencies
import laspy as lp
#import liblas
import tkinter as tk
from PIL import Image, ImageTk

# Tkinter example code
## example of using opencv array as tkimage:
## https://stackoverflow.com/questions/28670461/read-an-image-with-opencv-and-display-it-with-tkinter

width  = 640
height = 480

class SL_Scanner(tk.Tk):
    def __init__(self, width, height):
        self.counter = 0
        tk.Tk.__init__(self)
        tk.Tk.title(self,"Structued light demo")
        tk.Tk.geometry(self,f"{width}x{height}")
        # genetate structured light frames
        self.gray = sl.Gray() 
        self.imglist = []    
        self.imlist_pattern = self.gray.generate((width, height))
        for c,v in enumerate(self.imlist_pattern):
            self.imglist.append(ImageTk.PhotoImage(Image.fromarray(v)))
            print(f"image {c} converted")
        
        self.imageLabel = tk.Label(self, image=self.imglist[0])
        self.infoLabel = tk.Label(self, text=f"Image 0 of {len(self.imglist)}", font="Helvetica, 20")    
        self.imageLabel.pack()
        self.infoLabel.pack()
        self.update_image()

    def update_image(self):    
        if self.counter < len(self.imglist) - 1:
            self.counter += 1
        else:
            self.counter = 0
        self.imageLabel.config(image=self.imglist[self.counter])
        self.infoLabel.config(text="Image " + str(self.counter + 1) + " of " + str(len(self.imglist)))
        self.after(1000,self.update_image)

def decode_captures():
    #    imlist_captured = imlist_pattern
    #
    #    img_index = gray.decode(imlist_captured, thresh=127)
    #
    #    print(img_index)
    pass


if __name__== "__main__":
    app = SL_Scanner(width, height)
    app.mainloop()




