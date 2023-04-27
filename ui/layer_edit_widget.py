import tkinter as tk
from PIL import Image, ImageTk
import cv2 as cv
import numpy as np

class LayerEditWidget():
    def __init__(self, master, layer_object, update_function, call_button) -> None:
        self.layer_object = layer_object
        self.master = master
        self.update_function = update_function
        self.call_button = call_button
        self.call_button["state"] == "disabled"

        self.window_edit_layer=tk.Toplevel(self.master)

        self.width = 800
        self.scalar = self.width/self.layer_object.mask.shape[1]

        self.canvas = tk.Canvas(self.window_edit_layer, width=self.width, height=self.scalar*self.layer_object.mask.shape[0], bg="white")
        height = int(self.layer_object.mask.shape[0]*self.scalar)
        width =  int(self.layer_object.mask.shape[1]*self.scalar)


        self.image_pil = Image.fromarray(cv.cvtColor(self.layer_object.original_image, cv.COLOR_BGR2RGB)).resize((width,height)) #Image.open("img/gaya.png")#
        self.image_tk = ImageTk.PhotoImage(self.image_pil)
        self.canvas_image_tk = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)

    
        mask = (self.layer_object.mask * 255).astype(np.uint8)
        mask = cv.cvtColor(mask, cv.COLOR_GRAY2RGB)        
        h, w, c = mask.shape
        mask_a = np.concatenate([mask, np.full((h, w, 1), 255, dtype=np.uint8)], axis=-1)
        white = np.all(mask == [255, 255, 255], axis=-1)
        mask_a[white, -1] = 0

        self.mask_pil = Image.fromarray(mask_a).resize((width,height)) #Image.open("img/gaya.png")#
        self.mask_tk = ImageTk.PhotoImage(self.mask_pil)
        self.canvas_mask_tk = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.mask_tk) 

        self.canvas.pack()

        self.button_finish = tk.Button(master=self.window_edit_layer, text="Save", command=self.finish_callback)
        self.button_finish.pack()


        self.x = 0
        self.y = 0

        self.window_edit_layer.bind("<KeyPress-Left>", lambda e: self.left(e))
        self.window_edit_layer.bind("<KeyPress-Right>", lambda e: self.right(e))
        self.window_edit_layer.bind("<KeyPress-Up>", lambda e: self.up(e))
        self.window_edit_layer.bind("<KeyPress-Down>", lambda e: self.down(e))
        self.movement()
     
    def movement(self):
 
        self.canvas.move(self.canvas_image_tk, self.x, self.y)
        self.x = 0
        self.y = 0
        self.canvas.after(100, self.movement)


    def left(self, event):
        self.x = -5
        self.y = 0
     
    def right(self, event):
        self.x = 5
        self.y = 0
     
    def up(self, event):
        self.x = 0
        self.y = -5
     
    def down(self, event):
        self.x = 0
        self.y = 5
        
    def finish_callback(self):
        self.button_finish["state"] = "disabled"
        image_scalar = self.width/self.layer_object.original_image.shape[1]

        (translate_x, translate_y) = np.array(self.canvas.coords(self.canvas_image_tk))
        translate_x = int(translate_x/image_scalar)
        translate_y = int(translate_y/image_scalar)
        output = self.layer_object.original_image
        #right
        if translate_x > 0:
            output = cv.copyMakeBorder(output, left=abs(translate_x), right=0, top=0, bottom=0, borderType=cv.BORDER_CONSTANT,value=[1,1,1])
            output = output[:, 0 : output.shape[1]-abs(translate_x)]
        #left
        elif translate_x < 0:
            output = cv.copyMakeBorder(output, left=0, right=abs(translate_x), top=0, bottom=0, borderType=cv.BORDER_CONSTANT,value=[1,1,1])
            output = output[:, abs(translate_x): output.shape[1]]

        #up
        if translate_y < 0:
            output = cv.copyMakeBorder(output, left=0, right=0, top=0, bottom=abs(translate_y), borderType=cv.BORDER_CONSTANT,value=[1,1,1])
            output = output[abs(translate_y):output.shape[0], : ]

        #down
        elif translate_y > 0:
            output = cv.copyMakeBorder(output, left=0, right=0, top=abs(translate_y), bottom=0, borderType=cv.BORDER_CONSTANT,value=[1,1,1])
            output = output[0:output.shape[0] - abs(translate_y), : ]

        self.layer_object.update_image(output)
        self.update_function()
        self.call_button["state"] == "normal"
        self.window_edit_layer.destroy()



