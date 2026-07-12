# UI/admin/admin_home.py

import tkinter as tk
from UI.styles import (
    BG_CARD, ACCENT, BTN_BLUE, BTN_GREY, TEXT_WHITE, TEXT_MUTED,
    FONT_TITLE, FONT_SUBTITLE, FONT_BTN,
    set_background, get_asset_path, place_on_canvas
)


class AdminHome:
    def __init__(self, root, main_root):
        self.root      = root
        self.main_root = main_root
        self.root.title("Admin — Home")
        self.root.state("zoomed")
        self.root.resizable(True, True)
        self.root.protocol("WM_DELETE_WINDOW", self.go_back)
        self.build_ui()

    def build_ui(self):
        canvas = set_background(
            self.root,
        get_asset_path("admin", "admin_page.png")
        )

        outer = tk.Frame(canvas, bg=BG_CARD, padx=50, pady=40)

        tk.Label(outer, text="ADMIN PANEL",
                 font=FONT_TITLE, bg=BG_CARD,
                 fg=ACCENT).grid(row=0, column=0, pady=(0, 6))
        tk.Label(outer, text="Registration or Login to continue",
                 font=FONT_SUBTITLE, bg=BG_CARD,
                 fg=TEXT_MUTED).grid(row=1, column=0, pady=(0, 24))

        btn_cfg = dict(font=FONT_BTN, width=26, height=2,
                       bd=0, cursor="hand2", relief="flat")

        tk.Button(outer, text="📝   REGISTRATION",
                  bg=BTN_BLUE, fg=TEXT_WHITE,
                  command=self.open_register,
                  **btn_cfg).grid(row=2, column=0, pady=8, sticky="ew")

        tk.Button(outer, text="🔐   LOGIN",
                  bg=ACCENT, fg=TEXT_WHITE,
                  command=self.open_login,
                  **btn_cfg).grid(row=3, column=0, pady=8, sticky="ew")

        tk.Button(outer, text="⬅   BACK",
                  bg=BTN_GREY, fg=TEXT_WHITE,
                  command=self.go_back,
                  **btn_cfg).grid(row=4, column=0, pady=8, sticky="ew")

        place_on_canvas(canvas, outer)

    def open_register(self):
        from UI.admin.admin_register import AdminRegister
        self.root.withdraw()
        top = tk.Toplevel(self.root)
        AdminRegister(top, self.root)

    def open_login(self):
        from UI.admin.admin_login import AdminLogin
        self.root.withdraw()
        top = tk.Toplevel(self.root)
        AdminLogin(top, self.root)

    def go_back(self):
        self.root.destroy()
        self.main_root.deiconify()