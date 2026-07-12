import tkinter as tk
from PIL import Image, ImageTk


class BaseWindow2:
    
    def __init__(self, root, bg_image_path):
        self.root = root
        self.bg_image_path = bg_image_path

        self.canvas = tk.Canvas(root, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.frame = tk.Frame(self.canvas, bg="")  # UI container

        self.canvas.create_window(0, 0, anchor="nw", window=self.frame)

        self.root.bind("<Configure>", self.resize_bg)

        self.load_bg()

    def load_bg(self):
        self.original_img = Image.open(self.bg_image_path)
        self.bg_photo = None
        self.resize_bg()

    def resize_bg(self, event=None):
        w = self.root.winfo_width()
        h = self.root.winfo_height()

        img = self.original_img.resize((w, h))
        self.bg_photo = ImageTk.PhotoImage(img)

        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

    def get_frame(self):
        return self.frame