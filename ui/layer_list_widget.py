import tkinter as tk

class LayersList():
    def __init__(self,master) -> None:
        self.frame_layers = tk.Frame(
            master=master,
            relief=tk.RAISED,
            borderwidth=1,
            background="red"
        )
        self.frame_layers.pack(fill="both", expand=True)

    def update_layers(self,layers):
        # for widget in self.frame_layers.winfo_children():
        #     widget.pack_forget()

        for widget in layers:
            widget.pack()