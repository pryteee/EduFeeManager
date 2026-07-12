import tkinter as tk
from PIL import Image, ImageTk


class BaseWindow:
    def __init__(self, root, image_path):
        self.root = root
        self.image_path = image_path

        self.canvas = tk.Canvas(root, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.frame = tk.Frame(self.canvas, bg="")

        self.canvas.create_window(0, 0, anchor="nw", window=self.frame)

        self.root.bind("<Configure>", self.resize_bg)
        self.load_image()

    def load_image(self):
        self.img = Image.open(self.image_path)

    def resize_bg(self, event=None):
        w = self.root.winfo_width()
        h = self.root.winfo_height()

        img = self.img.resize((w, h))
        self.bg = ImageTk.PhotoImage(img)

        self.canvas.create_image(0, 0, image=self.bg, anchor="nw")

    def get_frame(self):
        return self.frame