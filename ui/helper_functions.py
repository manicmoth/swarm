from tkinter.filedialog import askopenfilename

def open_image(title = "Choose an image"):
    filename = askopenfilename(filetypes=[('Images','*.jpg *.jpeg *.png')], title=title)
    return filename

accent_color = "#436764"