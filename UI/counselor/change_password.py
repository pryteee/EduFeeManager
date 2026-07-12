# views/counselor/change_password.py

import tkinter as tk
from tkinter import messagebox
from models.counselor_model import CounselorModel
from UI.styles import (
    BG_DARK, BG_CARD, BG_INPUT, ACCENT, BTN_GREY,
    TEXT_WHITE, TEXT_MUTED, FONT_TITLE, FONT_SUBTITLE,
    FONT_LABEL, FONT_ENTRY, FONT_BTN, ENTRY_W, PAD_Y,
    set_background, get_asset_path, place_on_canvas
)


class CounselorChangePassword:
    def __init__(self, root, prev_root):
        self.root      = root
        self.prev_root = prev_root
        self.model     = CounselorModel()
        self.root.title("Counselor — Change Password")
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

        tk.Label(outer, text="CHANGE PASSWORD",
                 font=FONT_TITLE, bg=BG_DARK, fg=ACCENT).grid(row=0, column=0, pady=(0, 4))
        tk.Label(outer, text="Enter your old password to set a new one",
                 font=FONT_SUBTITLE, bg=BG_DARK, fg=TEXT_MUTED).grid(row=1, column=0, pady=(0, 20))

        card = tk.Frame(outer, bg=BG_CARD, padx=50, pady=40)
        card.grid(row=2, column=0)

        self.counselor_id_var     = tk.StringVar()
        self.username_var    = tk.StringVar()
        self.old_var     = tk.StringVar()
        self.new_var     = tk.StringVar()
        self.confirm_var = tk.StringVar()

        fields = [
            ("Counselor ID",     self.counselor_id_var,     False),
            ("username",         self.username_var,    False),
            ("Old Password",     self.old_var,     True),
            ("New Password",     self.new_var,     True),
            ("Confirm Password", self.confirm_var, True),
        ]
        for i, (label, var, is_pass) in enumerate(fields):
            tk.Label(card, text=label, font=FONT_LABEL,
                     bg=BG_CARD, fg=TEXT_WHITE, anchor="w"
                     ).grid(row=i*2, column=0, sticky="w", pady=(PAD_Y, 0))
            tk.Entry(card, textvariable=var, width=ENTRY_W,
                     show="*" if is_pass else "",
                     font=FONT_ENTRY, bg=BG_INPUT, fg=TEXT_WHITE,
                     insertbackground=TEXT_WHITE, relief="flat", bd=6
                     ).grid(row=i*2+1, column=0, sticky="ew", pady=(0, PAD_Y))

        n = len(fields)
        btn_cfg = dict(font=FONT_BTN, width=22, height=2, bd=0, cursor="hand2", relief="flat")
        tk.Button(card, text="UPDATE PASSWORD", bg=ACCENT,   fg=TEXT_WHITE, command=self.update,   **btn_cfg).grid(row=n*2, column=0, sticky="ew", pady=(16, 6))
        tk.Button(card, text="⬅  BACK",         bg=BTN_GREY, fg=TEXT_WHITE, command=self.go_back,  **btn_cfg).grid(row=n*2+1, column=0, sticky="ew")
        place_on_canvas(canvas, outer)
    def update(self):
        try:
            counselor_id = int(self.counselor_id_var.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Counselor ID must be a number!", parent=self.root)
            return
        username    = self.username_var.get().strip()
        old     = self.old_var.get().strip()
        new     = self.new_var.get().strip()
        confirm = self.confirm_var.get().strip()
        if not all([username, old, new, confirm]):
            messagebox.showerror("Error", "All fields required!", parent=self.root)
            return
        if new != confirm:
            messagebox.showerror("Error", "Passwords do not match!", parent=self.root)
            return
        success = self.model.change_password(counselor_id, username, old, new)
        if success:
            messagebox.showinfo("Success", "Password changed!", parent=self.root)
            self.go_back()
        else:
            messagebox.showerror("Error", "Incorrect ID, usernamename or Old Password!", parent=self.root)

    def go_back(self):
        self.root.destroy()
        self.prev_root.deiconify()