# views/student/forgot_password.py

import tkinter as tk
from tkinter import messagebox
from models.student_model import StudentModel
from UI.styles import (
    BG_DARK, BG_CARD, BG_INPUT, ACCENT, BTN_BLUE, BTN_GREY,
    TEXT_WHITE, TEXT_MUTED, FONT_TITLE, FONT_SUBTITLE,
    FONT_LABEL, FONT_ENTRY, FONT_BTN, ENTRY_W, PAD_Y
)


class StudentForgotPassword:
    def __init__(self, root, prev_root):
        self.root      = root
        self.prev_root = prev_root
        self.model     = StudentModel()
        self.found     = None
        self.root.title("Student — Forgot Password")
        self.root.state("zoomed")
        self.root.configure(bg=BG_DARK)
        # self.root.resizable(True, True)
        self.root.protocol("WM_DELETE_WINDOW", self.go_back)
        self.build_ui()
        self.root.state('zoomed')

    def build_ui(self):
        outer = tk.Frame(self.root, bg=BG_DARK)
        outer.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(outer, text="FORGOT PASSWORD",
                 font=FONT_TITLE, bg=BG_DARK, fg=ACCENT).grid(row=0, column=0, pady=(0, 4))
        tk.Label(outer, text="Verify with Student ID and Email",
                 font=FONT_SUBTITLE, bg=BG_DARK, fg=TEXT_MUTED).grid(row=1, column=0, pady=(0, 20))

        card = tk.Frame(outer, bg=BG_CARD, padx=50, pady=40)
        card.grid(row=2, column=0)

        self.sid_var     = tk.StringVar()
        self.email_var   = tk.StringVar()
        self.new_var     = tk.StringVar()
        self.confirm_var = tk.StringVar()

        entry_cfg = dict(width=ENTRY_W, font=FONT_ENTRY, bg=BG_INPUT,
                         fg=TEXT_WHITE, insertbackground=TEXT_WHITE, relief="flat", bd=6)
        lbl_cfg   = dict(font=FONT_LABEL, bg=BG_CARD, fg=TEXT_WHITE, anchor="w")
        btn_cfg   = dict(font=FONT_BTN, width=22, height=2, bd=0, cursor="hand2", relief="flat")

        tk.Label(card, text="Student ID", **lbl_cfg).grid(row=0, column=0, sticky="w", pady=(PAD_Y, 0))
        tk.Entry(card, textvariable=self.sid_var, **entry_cfg).grid(row=1, column=0, sticky="ew", pady=(0, PAD_Y))
        tk.Label(card, text="Email",      **lbl_cfg).grid(row=2, column=0, sticky="w", pady=(PAD_Y, 0))
        tk.Entry(card, textvariable=self.email_var, **entry_cfg).grid(row=3, column=0, sticky="ew", pady=(0, PAD_Y))

        tk.Button(card, text="VALIDATE IDENTITY", bg=BTN_BLUE, fg=TEXT_WHITE,
                  command=self.validate, **btn_cfg).grid(row=4, column=0, sticky="ew", pady=(4, 16))

        tk.Label(card, text="── Set New Password ──",
                 font=FONT_LABEL, bg=BG_CARD, fg=TEXT_MUTED).grid(row=5, column=0, pady=(0, 6))

        tk.Label(card, text="New Password",      **lbl_cfg).grid(row=6, column=0, sticky="w", pady=(PAD_Y, 0))
        tk.Entry(card, textvariable=self.new_var, show="*", **entry_cfg).grid(row=7, column=0, sticky="ew", pady=(0, PAD_Y))
        tk.Label(card, text="Confirm Password",  **lbl_cfg).grid(row=8, column=0, sticky="w", pady=(PAD_Y, 0))
        tk.Entry(card, textvariable=self.confirm_var, show="*", **entry_cfg).grid(row=9, column=0, sticky="ew", pady=(0, PAD_Y))

        tk.Button(card, text="RESET PASSWORD", bg=ACCENT,   fg=TEXT_WHITE, command=self.reset,     **btn_cfg).grid(row=10, column=0, sticky="ew", pady=(12, 6))
        tk.Button(card, text="⬅  BACK",        bg=BTN_GREY, fg=TEXT_WHITE, command=self.go_back,   **btn_cfg).grid(row=11, column=0, sticky="ew")

    def validate(self):
        try:
            sid = int(self.sid_var.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Enter valid Student ID!", parent=self.root)
            return
        email = self.email_var.get().strip()
        if not email:
            messagebox.showerror("Error", "Enter email!", parent=self.root)
            return
        self.found = self.model.validate_forgot_password(sid, email)
        if self.found:
            messagebox.showinfo("Validated", "Identity verified!", parent=self.root)
        else:
            messagebox.showerror("Error", "No match found!", parent=self.root)

    def reset(self):
        if not self.found:
            messagebox.showerror("Error", "Validate first!", parent=self.root)
            return
        new  = self.new_var.get().strip()
        conf = self.confirm_var.get().strip()
        if not new or not conf:
            messagebox.showerror("Error", "Enter new password!", parent=self.root)
            return
        if new != conf:
            messagebox.showerror("Error", "Passwords do not match!", parent=self.root)
            return
        success = self.model.update_password_by_id(self.found['student_id'], new)
        if success:
            messagebox.showinfo("Success", "Password reset successfully!", parent=self.root)
            self.go_back()
        else:
            messagebox.showerror("Error", "Reset failed!", parent=self.root)

    def go_back(self):
        self.root.destroy()
        self.prev_root.deiconify()