import tkinter as tk

class OutputImage():
    def __init__(self,master,output_image) -> None:
        """
        master - tk master
        output_image - cv image as background for image layer
        """
        self.frame_output_image = tk.Frame(
            master=master,
            relief=tk.RAISED,
            borderwidth=1,
            background="blue"
        )
        self.frame_output_image.pack()

        #add output image
        self.label_output_image = tk.Label(master=self.frame_output_image, image=output_image)
        self.label_output_image.pack()

    def update_image(self,image):
        """
        Display new image
        image - PIL image
        """
        self.label_output_image.configure(image=image)
        self.label_output_image.image=image

    def get_dimensions(self):
        """
        Returns int (width,height) of frame
        """
        return (self.frame_output_image.winfo_width(), self.frame_output_image.winfo_height())