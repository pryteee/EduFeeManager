# views/styles.py

import os
import tkinter as tk
from tkinter import PhotoImage

# Colors
BG_DARK      = "#1a1a2e"
BG_CARD      = "#16213e"
BG_INPUT     = "#0f3460"
ACCENT       = "#e94560"
BTN_BLUE     = "#0f3460"
BTN_GREY     = "#3a3a4a"
TEXT_WHITE   = "#ffffff"
TEXT_MUTED   = "#a8a8b3"
TEXT_SUCCESS = "#00c851"
TEXT_WARN    = "#ffbb33"
TEXT_DANGER  = "#e94560"

# Fonts
FONT_TITLE    = ("Helvetica", 22, "bold")
FONT_SUBTITLE = ("Helvetica", 13)
FONT_LABEL    = ("Helvetica", 11)
FONT_ENTRY    = ("Helvetica", 12)
FONT_BTN      = ("Helvetica", 11, "bold")
FONT_BTN_SM   = ("Helvetica", 10)
FONT_MONO     = ("Courier", 11)

# Sizes
BTN_W  = 22
BTN_H  = 2
ENTRY_W = 36
PAD_X  = 20
PAD_Y  = 6

# ─────────────────────────────────────────────────────────
# BASE PATH — resolves asset path regardless of working dir
# ─────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_asset_path(subfolder, filename):
    """
    Returns full path to an asset file.
    subfolder = 'admin' | 'counselor' | 'student'
    filename  = 'admin_home_bg.png'
    """
    return os.path.join(BASE_DIR, "assets", subfolder, filename)


def set_background(root, image_path):
    """
    Places a full-window background image on any Tkinter window.
    Returns the Canvas so widgets can be placed on it.

    Usage:
        canvas = set_background(self.root, get_asset_path('admin', 'admin_home_bg.png'))
        frame  = tk.Frame(canvas, ...)
        canvas.create_window(x, y, window=frame, anchor='center')
    """
    try:
        from PIL import Image, ImageTk

        # Load and resize image to fill the screen
        screen_w = root.winfo_screenwidth()
        screen_h = root.winfo_screenheight()

        img = Image.open(image_path)
        img = img.resize((screen_w, screen_h), Image.LANCZOS)
        bg_image = ImageTk.PhotoImage(img)

        canvas = tk.Canvas(root, width=screen_w, height=screen_h,
                           highlightthickness=0, bd=0)
        canvas.pack(fill="both", expand=True)
        canvas.create_image(0, 0, anchor="nw", image=bg_image)

        # IMPORTANT: keep reference so Python doesn't garbage collect it
        canvas.bg_image = bg_image
        canvas.screen_w = screen_w
        canvas.screen_h = screen_h

        return canvas

    except FileNotFoundError:
        # If image missing — fallback to solid color, no crash
        root.configure(bg=BG_DARK)
        canvas = tk.Canvas(root, bg=BG_DARK,
                           highlightthickness=0, bd=0)
        canvas.pack(fill="both", expand=True)
        canvas.screen_w = root.winfo_screenwidth()
        canvas.screen_h = root.winfo_screenheight()
        return canvas

    except ImportError:
        # Pillow not installed — fallback
        root.configure(bg=BG_DARK)
        canvas = tk.Canvas(root, bg=BG_DARK,
                           highlightthickness=0, bd=0)
        canvas.pack(fill="both", expand=True)
        canvas.screen_w = root.winfo_screenwidth()
        canvas.screen_h = root.winfo_screenheight()
        return canvas


def place_on_canvas(canvas, frame):
    """
    Centers a frame on the canvas at screen center.
    Call this AFTER building all widgets inside the frame.
    """
    canvas.update_idletasks()
    x = canvas.screen_w // 2
    y = canvas.screen_h // 2
    canvas.create_window(x, y, window=frame, anchor="center")