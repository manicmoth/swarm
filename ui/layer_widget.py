import tkinter as tk
from PIL import ImageTk, Image  
import cv2 as cv
import numpy as np


class LayerWidget():
    def __init__(self, master, name, layer_object) -> None:
        self.master = master
        self.layer_object = layer_object
        self.name = name
        self.frame_layer = tk.Frame(
            master=master,
            relief=tk.RAISED,
            borderwidth=1,
            background="white"
        )
        self.label_frame_name = tk.Label(master=self.frame_layer,text=self.name) 

           
        self.mask = Image.fromarray(layer_object.mask)
        self.mask.convert('RGB')
        self.mask.thumbnail([self.master.winfo_width(), 30])#mask.height])
        self.mask = ImageTk.PhotoImage(self.mask)

        self.overlay = Image.fromarray(cv.cvtColor(layer_object.image, cv.COLOR_BGR2RGB))
        self.overlay.thumbnail([self.master.winfo_width(), 30])#overlay.height])
        self.overlay = ImageTk.PhotoImage(self.overlay)

        self.image_mask = tk.Label(master=self.frame_layer, image=self.mask)
        self.image_overlay = tk.Label(master=self.frame_layer, image=self.overlay)

        self.label_frame_name.grid(row=0,column=0, columnspan = 1, padx=5,pady=5, sticky="ne")       
        self.image_mask.grid(row=0,column=1, columnspan = 1, padx=5,pady=5, sticky="ne")       
        self.image_overlay.grid(row=0,column=2, columnspan = 1, padx=5,pady=5, sticky="ne")       

    def pack(self):
        self.frame_layer.pack()

    def pack_forget(self):
        self.frame_layer.pack_forget()

    def update_overlay():
        pass
