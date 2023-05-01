import sys
from os import getcwd

sys_path = getcwd()
sys.path.insert(1, sys_path)

import tkinter as tk
from tkinter.filedialog import askopenfilename
from swarm.layer import Image_Layer
from swarm.layer import Operation
from swarm.detectron_segmenter import Segmenter
from helper_functions import open_image, accent_color
import cv2 as cv
from PIL import ImageTk, Image  
import numpy as np 
from layer_widget import LayerWidget
from output_image_widget import OutputImage
from layer_list_widget import LayersList

class UserInterface():
    def __init__(self) -> None:
        self.segmenter = Segmenter()
        self.window = tk.Tk()

        self.window.rowconfigure(0, weight=1, minsize=400)
        for i in range(3):
            self.window.columnconfigure(i, weight=1, minsize=300)

        self.frame_output = tk.Frame(
            master=self.window,
            relief=tk.RAISED,
            borderwidth=1,
            background=accent_color,
        )
        self.frame_output.grid(row=0, column=0, columnspan = 2, padx=5,pady=5, sticky="nsew")

        #define add background button
        self.button_choose_background = tk.Button(master=self.frame_output, text="Choose Background Image", command=self.choose_background_callback)
        self.button_choose_background.pack()

        self.button_download_output = tk.Button(master=self.frame_output, text="Download Output", command=self.download_output_callback)
        self.button_download_output.pack()

        #create background image with default background
        output_image = cv.imread("img/black_image.png")
        self.background_layer = Image_Layer(image=output_image)
        self.output_image = (Image.fromarray(output_image))
        output_image =  ImageTk.PhotoImage(self.output_image)
        self.background = OutputImage(master=self.frame_output, output_image=output_image)


        self.frame_layer_wrapper = tk.Frame(self.window)
        self.frame_layer_wrapper.grid(row=0, column=2, columnspan = 1, padx=5,pady=5, sticky="nsew")

        # canvas
        self.canvas_layers = tk.Canvas(self.frame_layer_wrapper)
        self.canvas_layers.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        # scrollbar
        self.scrollbar = tk.Scrollbar(self.frame_layer_wrapper, orient=tk.VERTICAL, command=self.canvas_layers.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y) 

        self.canvas_layers.configure(yscrollcommand=self.scrollbar.set)
        self.canvas_layers.bind('<Configure>', lambda e: self.canvas_layers.configure(scrollregion=self.canvas_layers.bbox("all")))

        self.frame_layers = tk.Frame(
            master=self.canvas_layers,
            relief=tk.RAISED,
            borderwidth=1,
        )
        self.canvas_layers.create_window((0, 0), window=self.frame_layers, anchor="nw")
        #set header test
        self.label_layers = tk.Label(master=self.frame_layers, text=f"Layer list")
        self.label_layers.pack()
        #setup button to add new layer
        self.button_new_layer = tk.Button(master=self.frame_layers, text="New Layer", command=self.new_layer_callback)
        self.button_new_layer.pack()

        #setup button to add new layer
        self.button_segment_image = tk.Button(master=self.frame_layers, text="Segment Image", command=self.segment_image_callback)
        self.button_segment_image.pack()

        self.layers_widget = LayersList(master=self.frame_layers)

        #create list of layers
        self.layers = []
        #list of tk labels of each layer
        self.new_layer = None
   
        # adding new layer window and buttons
        self.window_new_layer = None
        self.button_layer_image = None 
        self.button_layer_mask = None
        self.button_activate_new_layer = None
        self.button_cancel_new_layer = None

        self.window.mainloop()

    def choose_background_callback(self):
        im_path = open_image()
        im = cv.imread(im_path)
        self.background_layer.update_image(im)
        self.update_background_callback()


    def new_layer_callback(self):
        """
        popup new layer definition
        """
        self.button_new_layer["state"] = "disabled"
        self.window_new_layer=tk.Toplevel(self.window)
        self.window_new_layer.geometry("400x200")
        self.window_new_layer.title("New Layer")
        self.new_layer = Image_Layer()
        
        #Create a label in Toplevel window
        self.button_layer_mask = tk.Button(master=self.window_new_layer, text="Select Layer Mask", command=self.open_mask_callback)
        self.button_layer_mask.pack()

        self.button_layer_image = tk.Button(master=self.window_new_layer, text="Select Layer Image", command=self.open_image_callback)
        self.button_layer_image.pack()

        self.button_cancel_new_layer = tk.Button(master=self.window_new_layer, text="Cancel", command=self.close_new_layer_callback)
        self.button_cancel_new_layer.pack()

        self.button_activate_new_layer = tk.Button(master=self.window_new_layer, text="Add Layer", command=self.add_new_layer_callback)
        self.button_activate_new_layer["state"] = "disabled"
        self.button_activate_new_layer.pack()

    def open_mask_callback(self):
        """
        Open mask image
        """    
        filename = open_image("Select Layer Mask")
        mask = cv.imread(filename)
        self.new_layer.update_mask(mask)
        label_name = filename.split("/")[-1]
        label = tk.Label(master=self.window_new_layer, text=f"Mask image: {label_name}")
        label.pack()
        self.button_layer_mask["state"] = "disabled"
        if not(self.new_layer.image is None) and not(self.new_layer.mask is None):
            self.button_activate_new_layer["state"] = "normal"

    def open_image_callback(self):
        """
        Opens layer image
        """
        filename = open_image("Select Layer Image")
        image = cv.imread(filename)
        self.new_layer.update_image(image)
        name = filename.split("/")[-1].split(".")[0]
        if name == None:
            name = f"layer{len(self.layers)}"
        self.new_layer.set_name(name)
        label_name = filename.split("/")[-1]
        label = tk.Label(master=self.window_new_layer, text=f"Layer image: {label_name}")
        label.pack()
        self.button_layer_image["state"] = "disabled"
        if not(self.new_layer.image is None) and not(self.new_layer.mask is None):
            self.button_activate_new_layer["state"] = "normal"

    def close_new_layer_callback(self):
        self.new_layer = None
        self.window_new_layer.destroy()
        self.button_new_layer["state"] = "normal"

    def segment_image_callback(self):
        impath = open_image()
        im = cv.imread(impath)
        print(im)
        mask_list = self.segmenter.segment_image(im)

        for mask in mask_list:
            mask = np.array(mask, dtype=np.int8)
            overlay = cv.imread("img/white_image.png")
            name = f"layer {len(self.layers)}"
            new_layer = Image_Layer(image=overlay, mask=mask, name=name, operation_type=Operation.RESIZE_STRETCH)
            new_layer_wapper = LayerWidget(master=self.layers_widget.frame_layers, name=new_layer.name, layer_object=new_layer, update_function=self.update_background_callback)
            self.layers.append(new_layer_wapper)
        self.update_background_callback()
        self.layers_widget.update_layers(self.layers)

    def add_new_layer_callback(self):
        """
        Runs when new layer is added - adds layer to list and updates background image accordingly
        """
        #Create new layer wrapper widget
        new_layer = LayerWidget(self.layers_widget.frame_layers, self.new_layer.name, self.new_layer, update_function=self.update_background_callback)

        #Add new layer to list and update view
        self.layers.append(new_layer)
        self.update_background_callback()
        self.layers_widget.update_layers(self.layers)

        #reset state
        self.new_layer = None
        self.window_new_layer.destroy()
        self.button_new_layer["state"] = "normal"

    def update_background_callback(self):
        output_mask = cv.imread("img/black_image.png")
        output_mask = cv.cvtColor(output_mask, cv.COLOR_BGR2GRAY)
        print(output_mask)
        if len(self.layers) > 0:
            output_mask = cv.resize(output_mask, [self.layers[0].layer_object.mask.shape[1], self.layers[0].layer_object.mask.shape[0]])
            for layer in self.layers:
                if layer.layer_object.enabled:
                    mask = cv.resize(layer.layer_object.mask, [self.layers[0].layer_object.mask.shape[1], self.layers[0].layer_object.mask.shape[0]])
                    output_mask = np.add(output_mask, mask)
        output_mask = np.logical_not(output_mask).astype(int)
        self.background_layer.update_mask(output_mask)
        output = self.sum_images()

        resize_pil = Image.fromarray(cv.cvtColor(output, cv.COLOR_BGR2RGB))
        size = (self.background.get_dimensions()[0], self.background.get_dimensions()[1])
        resize_pil.thumbnail(size)
        self.output_image = resize_pil
        resize_pil = ImageTk.PhotoImage(resize_pil)
        self.background.update_image(resize_pil)

    def download_output_callback(self):
        self.output_image.save("output.png")


    def sum_images(self):
        output = cv.imread("img/black_image.png")
        if len(self.layers) > 0:
            output = cv.resize(output, [self.layers[0].layer_object.mask.shape[1], self.layers[0].layer_object.mask.shape[0]])
        for layer in self.layers:
            if layer.layer_object.enabled:
                image = cv.resize(layer.layer_object.get_masked_img(), [self.layers[0].layer_object.mask.shape[1], self.layers[0].layer_object.mask.shape[0]])
                output = np.add(output, image)
        output = np.add(output, self.background_layer.get_masked_img())
        return output

if __name__ == "__main__":
    ui = UserInterface()
