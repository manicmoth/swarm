import tkinter as tk
from layer import Image_Layer

class UserInterface():
    def __init__(self) -> None:
        self.window = tk.Tk(width=700, height=3500)
        self.window.rowconfigure(0, weight=1, minsize=50)
        for i in range(3):
            self.window.columnconfigure(i, weight=1, minsize=75)

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
        self.new_layer = Image_Layer()


        self.window.mainloop()


    def new_layer_callback(self):
        """
        popup new layer definition
        """
        top=tk.Toplevel(self.window)
        top.geometry("700x700")
        top.title("New Layer")
        #Create a label in Toplevel window
        tk.Button(master=top, text="Select Layer Mask", command=self.open_mask_callback)

    def open_mask_callback(self):
        """
        Open mask image
        """    
        filename = self.open_image("Select Layer Mask")

    def open_image(self, title = "Choose an image"):
        filename = tk.filedialog.askopenfilename(initialdir = "/",
                                            title = title,
                                            filetypes = (("Image files",
                                                            "*.jpg *.jpeg *.png")))
        return filename

if __name__ == "__main__":
    print("hihihi")
    ui = UserInterface()
    print(ui.layers)