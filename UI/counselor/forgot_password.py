import tkinter as tk
from tkinter import messagebox
from models.counselor_model import CounselorModel
from UI.styles import (
    BG_DARK, BG_CARD, BG_INPUT, ACCENT, BTN_BLUE, BTN_GREY,
    TEXT_WHITE, TEXT_MUTED, FONT_TITLE, FONT_SUBTITLE,
    FONT_LABEL, FONT_ENTRY, FONT_BTN, ENTRY_W, PAD_Y,
    set_background, get_asset_path, place_on_canvas
)


class CounselorForgotPassword:
    def __init__(self, root, prev_root):
        self.root      = root
        self.prev_root = prev_root
        self.model     = CounselorModel()
        self.found     = None
        self.root.title("Counselor — Forgot Password")
        self.root.state("zoomed")
        self.root.configure(bg=BG_DARK)
        # self.root.resizable(True, True)
        self.root.protocol("WM_DELETE_WINDOW", self.go_back)
        self.build_ui()
        self.root.state('zoomed')

    def build_ui(self):
        canvas = set_background(
            self.root,
            get_asset_path("counselor", "#image")
        )
        outer = tk.Frame(self.root, bg=BG_DARK)
        outer.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(outer, text="FORGOT PASSWORD",
                 font=FONT_TITLE, bg=BG_DARK, fg=ACCENT).grid(row=0, column=0, pady=(0, 4))
        tk.Label(outer, text="Verify identity then reset password",
                 font=FONT_SUBTITLE, bg=BG_DARK, fg=TEXT_MUTED).grid(row=1, column=0, pady=(0, 20))

        card = tk.Frame(outer, bg=BG_CARD, padx=50, pady=40)
        card.grid(row=2, column=0)

        self.user_var     = tk.StringVar()
        self.ec_var       = tk.StringVar()
        self.new_pass_var = tk.StringVar()
        self.conf_var     = tk.StringVar()

        entry_cfg = dict(width=ENTRY_W, font=FONT_ENTRY, bg=BG_INPUT,
                         fg=TEXT_WHITE, insertbackground=TEXT_WHITE, relief="flat", bd=6)
        lbl_cfg   = dict(font=FONT_LABEL, bg=BG_CARD, fg=TEXT_WHITE, anchor="w")
        btn_cfg   = dict(font=FONT_BTN, width=22, height=2, bd=0, cursor="hand2", relief="flat")

        tk.Label(card, text="Username",            **lbl_cfg).grid(row=0, column=0, sticky="w", pady=(PAD_Y, 0))
        tk.Entry(card, textvariable=self.user_var, **entry_cfg).grid(row=1, column=0, sticky="ew", pady=(0, PAD_Y))
        tk.Label(card, text="Email OR Contact",    **lbl_cfg).grid(row=2, column=0, sticky="w", pady=(PAD_Y, 0))
        tk.Entry(card, textvariable=self.ec_var,   **entry_cfg).grid(row=3, column=0, sticky="ew", pady=(0, PAD_Y))

        tk.Button(card, text="VALIDATE IDENTITY", bg=BTN_BLUE, fg=TEXT_WHITE,
                  command=self.validate, **btn_cfg).grid(row=4, column=0, sticky="ew", pady=(4, 16))

        tk.Label(card, text="── Set New Password ──",
                 font=FONT_LABEL, bg=BG_CARD, fg=TEXT_MUTED).grid(row=5, column=0, pady=(0, 6))

        tk.Label(card, text="New Password",              **lbl_cfg).grid(row=6,  column=0, sticky="w", pady=(PAD_Y, 0))
        tk.Entry(card, textvariable=self.new_pass_var, show="*", **entry_cfg).grid(row=7,  column=0, sticky="ew", pady=(0, PAD_Y))
        tk.Label(card, text="Confirm Password",          **lbl_cfg).grid(row=8,  column=0, sticky="w", pady=(PAD_Y, 0))
        tk.Entry(card, textvariable=self.conf_var,     show="*", **entry_cfg).grid(row=9,  column=0, sticky="ew", pady=(0, PAD_Y))

        tk.Button(card, text="UPDATE PASSWORD", bg=ACCENT,   fg=TEXT_WHITE, command=self.update_password, **btn_cfg).grid(row=10, column=0, sticky="ew", pady=(12, 6))
        tk.Button(card, text="⬅  BACK",         bg=BTN_GREY, fg=TEXT_WHITE, command=self.go_back,         **btn_cfg).grid(row=11, column=0, sticky="ew")
        place_on_canvas(canvas, outer)
    def validate(self):
        user = self.user_var.get().strip()
        ec   = self.ec_var.get().strip()
        if not user or not ec:
            messagebox.showerror("Error", "Fill all fields!", parent=self.root)
            return
        self.found = self.model.validate_forgot_password(user, ec)
        if self.found:
            messagebox.showinfo("Validated", "Identity verified!", parent=self.root)
        else:
            messagebox.showerror("Error", "No match found!", parent=self.root)

    def update_password(self):
        if not self.found:
            messagebox.showerror("Error", "Validate first!", parent=self.root)
            return
        new  = self.new_pass_var.get().strip()
        conf = self.conf_var.get().strip()
        if not new or not conf:
            messagebox.showerror("Error", "Enter password!", parent=self.root)
            return
        if new != conf:
            messagebox.showerror("Error", "Passwords do not match!", parent=self.root)
            return
        success = self.model.update_password_by_username(self.found['username'], new)
        if success:
            messagebox.showinfo("Success", "Password updated!", parent=self.root)
            self.go_back()
        else:
            messagebox.showerror("Error", "Update failed!", parent=self.root)

    def go_back(self):
        self.root.destroy()
        self.prev_root.deiconify()
