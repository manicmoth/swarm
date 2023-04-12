from tkinter.filedialog import askopenfilename

def open_image(title = "Choose an image"):
    filename = askopenfilename(filetypes=[('Images','*.jpg *.jpeg *.png')], title=title)
    return filename

def open_video(title = "Choose a video"):
    filename = askopenfilename(filetypes=[('Videos','*.mp4')], title=title)
    return filename

def open_file(title = "Choose a video or image"):
    filename = askopenfilename(filetypes=[('Videos','*.mp4'), ('Images', '*.jpg *.jpeg *.png')], title=title)
    return filename