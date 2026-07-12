import tkinter as tk
from PIL import Image, ImageTk

# COLORS
BG = "#0d1117"

TEXT_HERO = "#0b3f6b"
TEXT_ACCENT = "#1f5fa8"
TEXT_DIM = "#4a4a4a"
TEXT_MID = "#3d79b9"
TEXT_ROLE = "#47632F"

BTN_BG = "#123c7a"
BTN_FG = "#ffffff"


class WelcomePage:

    def __init__(self, root):
        self.root = root
        self.root.title("College Fee Structure Management System")
        self.root.configure(bg=BG)
        self.root.state("zoomed")

        self.root.bind("<Escape>", self.exit_fullscreen)

        self._canvas = tk.Canvas(
            self.root,
            bg=BG,
            highlightthickness=0
        )
        self._canvas.pack(fill="both", expand=True)

        self._canvas.bind("<Configure>", self._on_resize)

        
        self.bg_image = Image.open("background_3.png")

        self.bg_photo = None
        self.bg_id = self._canvas.create_image(
            0, 0,
            anchor="nw"
        )

        self._create_items()

    def exit_fullscreen(self, event=None):
        self.root.state("normal")

    # UI 
    def _create_items(self):
        cv = self._canvas

        self._badge_txt = cv.create_text(
            0, 0,
            text="",
            fill=TEXT_ROLE,
            font=("Helvetica", 10)
        )

        self._t1 = cv.create_text(
            0, 0,
            text="College Fee Structure",
            fill=TEXT_HERO,
            font=("Helvetica", 30, "bold")
        )

        self._t2 = cv.create_text(
            0, 0,
            text="Management System",
            fill=TEXT_ACCENT,
            font=("Helvetica", 28, "bold")
        )

        self._sub = cv.create_text(
            0, 0,
            text="SYSTEM DEVELOPED BY",
            fill=TEXT_DIM,
            font=("Helvetica", 16, "bold")
        )

        self._devby = cv.create_text(
            0, 0,
            text="TEAM LEADER",
            fill=TEXT_DIM,
            font=("Helvetica", 16)
        )

        self._leader = cv.create_text(
            0, 0,
            text="Ananya Subhadarshini Panda",
            fill=TEXT_HERO,
            font=("Helvetica", 18, "bold")
        )

        self._members = cv.create_text(
            0, 0,
            text="Pritirekha Panda  |  Nibedita Pal",
            fill=TEXT_MID,
            font=("Helvetica", 16)
        )

        # BUTTON 
        self.btn = tk.Button(
            self.root,
            text="PROCEED →",
            font=("Helvetica", 12, "bold"),
            bg=BTN_BG,
            fg=BTN_FG,
            activebackground=BTN_BG,
            activeforeground=BTN_FG,
            bd=0,
            padx=25,
            pady=10,
            cursor="hand2",
            command=self.open_main_menu
        )

        self.btn_window = cv.create_window(
            0, 0,
            window=self.btn
        )

    # RESIZE 
    def _on_resize(self, event=None):
        cv = self._canvas

        W = cv.winfo_width()
        H = cv.winfo_height()

        if W < 2 or H < 2:
            return

        # BACKGROUND
        resized = self.bg_image.resize(
            (W, H),
            Image.Resampling.LANCZOS
        )

        self.bg_photo = ImageTk.PhotoImage(resized)
        cv.itemconfig(self.bg_id, image=self.bg_photo)

        # TEXT POSITION 
        left_x = W * 0.25
        y = H * 0.24

        cv.coords(self._badge_txt, left_x, y - 60)

        cv.coords(self._t1, left_x, y)
        cv.coords(self._t2, left_x, y + 50)

        cv.coords(self._sub, left_x, y + 110)

        cv.coords(self._devby, left_x, y + 180)
        cv.coords(self._leader, left_x, y + 215)

        cv.coords(self._members, left_x, y + 255)

        cv.coords(self.btn_window, left_x, y + 340)


    def open_main_menu(self):
        self.root.destroy()

        from main import MainWindow

        new_root = tk.Tk()
        MainWindow(new_root)
        new_root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    WelcomePage(root)
    root.mainloop()