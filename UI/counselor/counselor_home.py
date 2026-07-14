import tkinter as tk
from UI.styles import (
    BG_DARK, BG_CARD, ACCENT, BTN_BLUE, BTN_GREY,
    TEXT_WHITE, TEXT_MUTED, FONT_TITLE, FONT_SUBTITLE, FONT_BTN,
    set_background, get_asset_path, place_on_canvas
)


class CounselorHome:
    def __init__(self, root, main_root):
        self.root      = root
        self.main_root = main_root
        self.root.title("Counselor — Home")
        self.root.state("zoomed")
        self.root.configure(bg=BG_DARK)
        # self.root.resizable(True, True)
        self.root.protocol("WM_DELETE_WINDOW", self.go_back)
        self.build_ui()
        self.root.state('zoomed')

    def build_ui(self):
        canvas = set_background(
            self.root,
            get_asset_path("counselor", "counselor_home.png")
        )
        outer = tk.Frame(self.root, bg=BG_DARK)
        outer.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(outer, text="COUNSELOR PANEL",
                 font=FONT_TITLE, bg=BG_DARK, fg=ACCENT).grid(row=0, column=0, pady=(0, 6))
        tk.Label(outer, text="Registration or Login to continue",
                 font=FONT_SUBTITLE, bg=BG_DARK, fg=TEXT_MUTED).grid(row=1, column=0, pady=(0, 30))

        card = tk.Frame(outer, bg=BG_CARD, padx=60, pady=40)
        card.grid(row=2, column=0)

        btn_cfg = dict(font=FONT_BTN, width=26, height=2, bd=0, cursor="hand2", relief="flat")
        tk.Button(card, text="📝   REGISTRATION", bg=BTN_BLUE, fg=TEXT_WHITE,
                  command=self.open_register, **btn_cfg).grid(row=0, column=0, pady=8)
        tk.Button(card, text="🔐   LOGIN",        bg=ACCENT,   fg=TEXT_WHITE,
                  command=self.open_login,    **btn_cfg).grid(row=1, column=0, pady=8)
        tk.Button(card, text="⬅   BACK",          bg=BTN_GREY, fg=TEXT_WHITE,
                  command=self.go_back,       **btn_cfg).grid(row=2, column=0, pady=8)
        place_on_canvas(canvas, outer)

    def open_register(self):
        from UI.counselor.counselor_register import CounselorRegister
        self.root.withdraw()
        top = tk.Toplevel(self.root)
        CounselorRegister(top, self.root)

    def open_login(self):
        from UI.counselor.counselor_login import CounselorLogin
        self.root.withdraw()
        top = tk.Toplevel(self.root)
        CounselorLogin(top, self.root)

    def go_back(self):
        self.root.destroy()
        self.main_root.deiconify()
