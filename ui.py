import tkinter as tk
from layer import Image_Layer



def new_layer_callback():
    """
    popup new layer definition
    """
    top=tk.Toplevel(window)
    top.geometry("700x250")
    top.title("New Layer")
    #Create a label in Toplevel window
    tk.Button(master=top, text="Select Layer Mask", command=open_mask_callback)

def open_mask_callback():
    """
    Open mask image
    """    
    filename = tk.filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("Text files",
                                                        "*.txt*"),
                                                       ("all files",
                                                        "*.*")))

window = tk.Tk()
window.rowconfigure(0, weight=1, minsize=50)
for i in range(3):
    window.columnconfigure(i, weight=1, minsize=75)

frame_output = tk.Frame(
    master=window,
    relief=tk.RAISED,
    borderwidth=1,
    background="blue"
)
frame_output.grid(row=0, column=0, columnspan = 2, padx=5,pady=5, sticky="nsew")
label_output = tk.Label(master=frame_output, text=f"Space for background image")
label_output.pack()


frame_label = tk.Frame(
    master=window,
    relief=tk.RAISED,
    borderwidth=1,
    background="red"
)
frame_label.grid(row=0, column=2, padx=5,pady=5, sticky="nsew")
label_layers = tk.Label(master=frame_label, text=f"Layer list")
label_layers.pack()
button_new_layer = tk.Button(master=frame_label, text="New Layer", command=new_layer_callback)

window.mainloop()