import os
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFont


BG_IMAGE_PATH = os.path.join("assets", "background.png")

"""
Utility that attaches a resizable background image to any Tkinter window.

Usage
-----
    from UI.bg_helper import attach_bg

    class MyPage:
        def __init__(self, root, ...):
            self._bg = attach_bg(root)   # call BEFORE build_ui
            self.build_ui()

The image must exist at:
    <project_root>/assets/bg_image.png

If the file is missing the function returns None and every page continues
to work normally with its solid-colour background.
"""

from pathlib import Path

_HERE       = Path(__file__).resolve().parent          
_ASSETS     = _HERE.parent / "assets"                  
BG_IMAGE_PATH = _ASSETS / "bg_image.png"


def attach_bg(window):
    """
    Place a full-window, auto-resizing background image on *window*.

    Parameters
    ----------
    window : tk.Tk | tk.Toplevel
        The root or top-level window to decorate.

    Returns
    -------
    PIL.ImageTk.PhotoImage | None
        Keep the returned object alive (e.g. ``self._bg = attach_bg(root)``)
        so Tkinter's garbage collector does not discard the image.
    """
    try:
        from PIL import Image, ImageTk   
    except ImportError:
        return None                       

    if not BG_IMAGE_PATH.exists():
        return None

    try:
        img = Image.open(BG_IMAGE_PATH)

        photo = ImageTk.PhotoImage(img)
        lbl   = window.nametowidget(window) if False else None   

        import tkinter as tk
        lbl = tk.Label(window, image=photo, bd=0, highlightthickness=0)
        lbl.image = photo
        lbl.place(x=0, y=0, relwidth=1, relheight=1)
        lbl.lower()

        def _on_resize(event):
            """Re-scale the image to fill the window whenever it is resized."""
            try:
                resized   = img.resize((event.width, event.height), Image.LANCZOS)
                new_photo = ImageTk.PhotoImage(resized)
                lbl.config(image=new_photo)
                lbl.image = new_photo          
            except Exception:
                pass

        window.bind("<Configure>", _on_resize, add="+")
        return photo

    except Exception:
        return None
def set_background(root, image_path=BG_IMAGE_PATH):
    """
    Adds a full-window background image to `root` (a Tk root or Toplevel).
    The image sits behind all other widgets and rescales on window resize.

    Must be called BEFORE other widgets are created/placed, so the
    background label is first in stacking order (i.e. behind everything).

    Returns the background Label (rarely needed by callers), or None if
    the image file could not be loaded (in which case the page's normal
    solid bg color is left untouched and nothing else breaks).
    """
    if not os.path.exists(image_path):
        
        print(f"[bg_helper] Background image not found at '{image_path}'. "
              f"Skipping background image for this window.")
        return None

    try:
        original = Image.open(image_path).convert("RGB")
    except Exception as e:
        print(f"[bg_helper] Could not open background image '{image_path}': {e}")
        return None

    bg_label = tk.Label(root, bd=0, highlightthickness=0)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    bg_label.lower() 

    state = {"original": original, "photo": None, "last_size": (0, 0)}

    def render(event=None):
        width  = root.winfo_width()
        height = root.winfo_height()
        if width <= 1 or height <= 1:
            return
        if state["last_size"] == (width, height):
            return 
        state["last_size"] = (width, height)

        resized = state["original"].resize((width, height), Image.LANCZOS)
        photo = ImageTk.PhotoImage(resized)
        state["photo"] = photo 
        bg_label.configure(image=photo)

    root.bind("<Configure>", render)
    root.update_idletasks()
    render()

    root._bg_state = state
    return bg_label


def shadow_label(parent, text, font, fg="#ffffff", shadow="#000000",
                  shadow_offset=(2, 2), padding=12, **place_kwargs):
    """
    Renders `text` with a drop-shadow onto a transparent image and shows
    it in a Label with NO visible rectangular background — so it reads
    clearly over a busy background image without a solid box behind it.

    Use this as a drop-in replacement for heading/subtitle tk.Label calls
    that currently sit directly on BG_DARK (i.e. outside the card).

    `font` should be a tuple like ("Helvetica", 28, "bold") — same as
    Tkinter's font tuples already used in this project's FONT_* constants.

    Any kwargs after `padding` (e.g. row=0, column=0, pady=(0, 4)) are
    forwarded to .grid() on the returned Label, so call sites can keep
    their existing grid positions unchanged. Pass place_kwargs=False-ish
    nothing to skip auto-gridding and place the label yourself.
    """
    font_name, font_size = font[0], font[1]
    font_style = font[2] if len(font) > 2 else "normal"

    is_bold = "bold" in str(font_style).lower()
    

    candidates = (
        ["arialbd.ttf", "Arial Bold.ttf"] if is_bold else ["arial.ttf", "Arial.ttf"]
    ) + [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if is_bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "DejaVuSans-Bold.ttf" if is_bold else "DejaVuSans.ttf",
    ]
    pil_font = None
    for candidate in candidates:
        try:
            pil_font = ImageFont.truetype(candidate, font_size)
            break
        except Exception:
            continue
    if pil_font is None:
        
        print("[bg_helper] No TTF font found for shadow_label; using PIL's "
              "tiny default font. Text size may look wrong.")
        pil_font = ImageFont.load_default()

    measure_img = Image.new("RGBA", (1, 1))
    measure_draw = ImageDraw.Draw(measure_img)
    bbox = measure_draw.textbbox((0, 0), text, font=pil_font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    canvas_w = text_w + abs(shadow_offset[0]) + padding * 2
    canvas_h = text_h + abs(shadow_offset[1]) + padding * 2

    img = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    base_x = padding - bbox[0]
    base_y = padding - bbox[1]

    draw.text((base_x + shadow_offset[0], base_y + shadow_offset[1]),
              text, font=pil_font, fill=shadow)
    draw.text((base_x, base_y), text, font=pil_font, fill=fg)

    photo = ImageTk.PhotoImage(img)

    label = tk.Label(parent, image=photo, bd=0, highlightthickness=0)
    label.image = photo

    if place_kwargs:
        label.grid(**place_kwargs)

    return label