from tkinter import Tk, BOTH
from tkinter import ttk
from ImageDisplay import ImageDisplayer
from PIL import Image, ImageTk

img_to_show = Image.open("temp/images/big_image.jpg")


# background_image = Image.open("background.png")


def start():
    root = Tk()
    root.resizable(height=True, width=True)
    root.state('zoomed')
    image_displayer = ImageDisplayer(root)
    image_displayer.load_image(img_to_show)
    image_displayer.pack(expand=True, fill=BOTH)
    root.mainloop()


start()
