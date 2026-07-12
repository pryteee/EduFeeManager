# UI/counselor/counselor_login.py

import tkinter as tk
from tkinter import messagebox
from models.counselor_model import CounselorModel
from UI.styles import (
    BG_DARK, BG_CARD, BG_INPUT, ACCENT, BTN_BLUE, BTN_GREY,
    TEXT_WHITE, TEXT_MUTED, FONT_TITLE, FONT_SUBTITLE,
    FONT_LABEL, FONT_ENTRY, FONT_BTN, ENTRY_W, PAD_Y,
    set_background, get_asset_path, place_on_canvas
)


class CounselorLogin:
    def __init__(self, root, prev_root):
        self.root      = root
        self.prev_root = prev_root
        self.model     = CounselorModel()
        self.root.title("Counselor — Login")
        self.root.state("zoomed")
        self.root.configure(bg=BG_DARK)
        # self.root.resizable(True, True)
        self.root.protocol("WM_DELETE_WINDOW", self.go_back)
        self.build_ui()
        self.root.state('zoomed')

    def build_ui(self):
        canvas = set_background(
            self.root,
            get_asset_path("admin", "#image")
        )
        outer = tk.Frame(self.root, bg=BG_DARK)
        outer.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(outer, text="COUNSELOR LOGIN",
                 font=FONT_TITLE, bg=BG_DARK, fg=ACCENT).grid(row=0, column=0, pady=(0, 4))
        tk.Label(outer, text="Enter your credentials",
                 font=FONT_SUBTITLE, bg=BG_DARK, fg=TEXT_MUTED).grid(row=1, column=0, pady=(0, 20))

        card = tk.Frame(outer, bg=BG_CARD, padx=50, pady=40)
        card.grid(row=2, column=0)

        self.user_var = tk.StringVar()
        self.pass_var = tk.StringVar()

        for i, (label, var, is_pass) in enumerate([
            ("Username", self.user_var, False),
            ("Password", self.pass_var, True),
        ]):
            tk.Label(card, text=label, font=FONT_LABEL,
                     bg=BG_CARD, fg=TEXT_WHITE, anchor="w"
                     ).grid(row=i*2, column=0, sticky="w", pady=(PAD_Y, 0))
            tk.Entry(card, textvariable=var, width=ENTRY_W,
                     show="*" if is_pass else "",
                     font=FONT_ENTRY, bg=BG_INPUT, fg=TEXT_WHITE,
                     insertbackground=TEXT_WHITE, relief="flat", bd=6
                     ).grid(row=i*2+1, column=0, sticky="ew", pady=(0, PAD_Y))

        btn_cfg = dict(font=FONT_BTN, width=22, height=2, bd=0, cursor="hand2", relief="flat")
        tk.Button(card, text="LOGIN",            bg=ACCENT,   fg=TEXT_WHITE, command=self.login,       **btn_cfg).grid(row=4, column=0, sticky="ew", pady=(16, 6))
        tk.Button(card, text="Forgot Password",  bg=BTN_BLUE, fg=TEXT_WHITE, command=self.open_forgot, **btn_cfg).grid(row=5, column=0, sticky="ew", pady=4)
        tk.Button(card, text="Change Password",  bg=BTN_BLUE, fg=TEXT_WHITE, command=self.open_change, **btn_cfg).grid(row=6, column=0, sticky="ew", pady=4)
        tk.Button(card, text="⬅  BACK",          bg=BTN_GREY, fg=TEXT_WHITE, command=self.go_back,     **btn_cfg).grid(row=7, column=0, sticky="ew", pady=(4, 0))
        place_on_canvas(canvas, outer)

    def login(self):
        user = self.user_var.get().strip()
        pwd  = self.pass_var.get().strip()
        if not user or not pwd:
            messagebox.showerror("Error", "All fields required!", parent=self.root)
            return
        result = self.model.login_counselor(user, pwd)
        if result:
            messagebox.showinfo("Success", f"Welcome, {result['name']}!", parent=self.root)
            from UI.counselor.manage_student import ManageStudent
            self.root.withdraw()
            top = tk.Toplevel(self.root)
            ManageStudent(top, self.root, result)
        else:
            messagebox.showerror("Error", "Invalid username or password!", parent=self.root)

    def open_forgot(self):
        from UI.counselor.forgot_password import CounselorForgotPassword
        self.root.withdraw()
        top = tk.Toplevel(self.root)
        CounselorForgotPassword(top, self.root)

    def open_change(self):
        from UI.counselor.change_password import CounselorChangePassword
        self.root.withdraw()
        top = tk.Toplevel(self.root)
        CounselorChangePassword(top, self.root)

    def go_back(self):
        self.root.destroy()
        self.prev_root.deiconify()