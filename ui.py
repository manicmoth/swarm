import tkinter as tk
from tkinter.filedialog import askopenfilename
from layer import Image_Layer
import cv2 as cv

class UserInterface():
    def __init__(self) -> None:
        self.window = tk.Tk()
        self.window.rowconfigure(0, weight=1, minsize=400)
        for i in range(3):
            self.window.columnconfigure(i, weight=1, minsize=300)

        self.frame_output = tk.Frame(
            master=self.window,
            relief=tk.RAISED,
            borderwidth=1,
            background="blue"
        )
        self.frame_output.grid(row=0, column=0, columnspan = 2, padx=5,pady=5, sticky="nsew")
        self.label_output = tk.Label(master=self.frame_output, text=f"Space for background image")
        self.label_output.pack()

        self.frame_label = tk.Frame(
            master=self.window,
            relief=tk.RAISED,
            borderwidth=1,
            background="red"
        )
        self.frame_label.grid(row=0, column=2, padx=5,pady=5, sticky="nsew")
        self.label_layers = tk.Label(master=self.frame_label, text=f"Layer list")
        self.label_layers.pack()
        self.button_new_layer = tk.Button(master=self.frame_label, text="New Layer", command=self.new_layer_callback)
        self.button_new_layer.pack()

        self.layers = []
        self.new_layer = None

        self.window_new_layer = None
        self.button_layer_image = None 
        self.button_layer_mask = None
        self.button_activate_new_layer = None
        self.button_cancel_new_layer = None

        self.window.mainloop()


    def new_layer_callback(self):
        """
        popup new layer definition
        """
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
        filename = self.open_image("Select Layer Mask")
        mask = cv.imread(filename)
        self.new_layer.update_mask(mask)
        label_name = filename.split("/")[-1]
        label = tk.Label(master=self.window_new_layer, text=f"Mask image: {label_name}")
        label.pack()
        self.button_layer_mask["state"] = "disabled"
        if not(self.new_layer.image is None) and not(self.new_layer.mask is None):
            self.button_activate_new_layer["state"] = "normal"

    def open_image_callback(self):
        filename = self.open_image("Select Layer Image")
        image = cv.imread(filename)
        self.new_layer.update_image(image)
        name = filename.split("/")[-1].split(".")[0]
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


    def open_image(self, title = "Choose an image"):
        filename = askopenfilename(filetypes=[('Images','*.jpg *.jpeg *.png')], title=title)
        return filename
    
    def add_new_layer_callback(self):
        self.layers.append(self.new_layer)
        label_layer = tk.Label(master=self.frame_label, text=self.new_layer.name)
        label_layer.pack()
        self.new_layer = None


if __name__ == "__main__":
    print("hihihi")
    ui = UserInterface()
    print(ui.layers)