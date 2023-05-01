import tkinter as tk
from PIL import ImageTk, Image  
import cv2 as cv
import numpy as np
from helper_functions import open_image, accent_color
from layer_edit_widget import LayerEditWidget


class LayerWidget():
    def __init__(self, master, name, layer_object, update_function) -> None:
        self.update_function = update_function
        self.master = master
        self.layer_object = layer_object
        self.name = name
        self.frame_layer = tk.Frame(
            master=master,
            relief=tk.RAISED,
            borderwidth=1,
            background=accent_color
        )


        self.label_frame_name = tk.Label(master=self.frame_layer, background=accent_color, fg="white", text=self.name) 
        self.button_edit = tk.Button(master=self.frame_layer, text="New Image", highlightbackground=accent_color, command=self.edit_layer_callback)
        self.button_adjust = tk.Button(master=self.frame_layer, text="Adjust", highlightbackground=accent_color,command=self.adjust_layer_callback)
        self.button_enable = tk.Button(master=self.frame_layer, text="Hide", highlightbackground=accent_color, command=self.enable_callback)

        self.window_edit_layer = None
        self.label_edit_overlay = None
        self.label_edit_mask = None     

        print(self.layer_object.mask)
        self.mask = Image.fromarray(self.layer_object.mask * 256)
        self.mask.convert('RGB')
        self.mask.thumbnail([self.master.winfo_width(), 30])#mask.height])


        self.mask_tk = ImageTk.PhotoImage(self.mask)

        self.overlay = Image.fromarray(cv.cvtColor(layer_object.image, cv.COLOR_BGR2RGB))
        self.overlay.thumbnail([self.master.winfo_width(), 30])#overlay.height])
        self.overlay_tk = ImageTk.PhotoImage(self.overlay)

        self.image_mask = tk.Label(master=self.frame_layer, image=self.mask_tk)
        self.image_overlay = tk.Label(master=self.frame_layer, image=self.overlay_tk)

        self.label_frame_name.grid(row=0,column=0, columnspan = 1, padx=5,pady=5, sticky="ne") 
        self.image_mask.grid(row=0,column=1, columnspan = 1, padx=5,pady=5, sticky="ne")       
        self.image_overlay.grid(row=0,column=2, columnspan = 1, padx=5,pady=5, sticky="ne")  
        self.button_adjust.grid(row=1,column=0, columnspan=1, padx=5, pady=5, sticky="ne")
        self.button_edit.grid(row=1,column=1, columnspan = 1, padx=5,pady=5, sticky="ne")       
        self.button_enable.grid(row=1,column=2, columnspan = 1, padx=5,pady=5, sticky="ne")  


        self.holder_image = None


    def pack(self):
        self.frame_layer.pack()

    def pack_forget(self):
        self.frame_layer.pack_forget()

    def edit_layer_callback(self):
        self.button_edit["state"] = "disabled"
        self.window_edit_layer=tk.Toplevel(self.master)
        self.window_edit_layer.geometry("400x200")
        self.window_edit_layer.title(f"Edit Layer {self.layer_object.name}")
        
        self.button_layer_image = tk.Button(master=self.window_edit_layer, text="Choose Layer Image", command=self.open_image_callback)
        self.button_layer_image.pack()
        
        self.label_image_name = tk.Label(master=self.window_edit_layer, text=f"Overlay: {self.name}")
        self.label_image_name.pack()

        self.button_activate_edit_layer = tk.Button(master=self.window_edit_layer, text="Update Layer", command=self.push_edit_layer_callback)
        self.button_activate_edit_layer.pack()
        self.button_activate_edit_layer["state"] = "disabled"

        self.button_cancel_edit_layer = tk.Button(master=self.window_edit_layer, text="Cancel", command=self.close_new_layer_callback)
        self.button_cancel_edit_layer.pack()

    def adjust_layer_callback(self):
        self.layer_edit_window = LayerEditWidget(master=self.master, 
                                                 layer_object=self.layer_object, 
                                                 update_function=self.update_function, 
                                                 call_button=self.button_adjust)




    def open_image_callback(self):
        holder_image_path = open_image("Choose new overlay")
        self.holder_image = cv.imread(holder_image_path)
        self.label_image_name.configure(text=holder_image_path)
        self.label_image_name.image=holder_image_path
        self.label_image_name.original_image=holder_image_path
        self.button_activate_edit_layer["state"] = "normal"

    def push_edit_layer_callback(self):
        """
        Runs when new layer is added - adds layer to list and updates background image accordingly
        """
        #Create new layer wrapper widget

        #Add new layer to list and update view

        #reset state
        self.layer_object.update_image(self.holder_image)
        self.layer_object.original_image = self.holder_image 


        self.overlay = Image.fromarray(cv.cvtColor(self.layer_object.image, cv.COLOR_BGR2RGB))
        self.overlay.thumbnail([self.master.winfo_width(), 30])#overlay.height])
        self.overlay_tk = ImageTk.PhotoImage(self.overlay)
        self.image_overlay.configure(image=self.overlay_tk)
        self.image_overlay.image=self.overlay_tk


        self.holder_image = None
        self.button_edit["state"] = "normal"
        self.pack()
        self.update_function()        
        self.window_edit_layer.destroy()



    def close_new_layer_callback(self):
        self.holder_image = None
        self.button_edit["state"] = "normal"
        self.window_edit_layer.destroy()


    def enable_callback(self):
        if self.layer_object.enabled:
            self.layer_object.enabled = False
            self.button_enable.config(text="Show", background="Green")
        else:
            self.layer_object.enabled = True
            self.button_enable.config(text="Hide", background="White")
        self.update_function()