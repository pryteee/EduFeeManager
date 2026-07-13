import tkinter as tk
from tkinter import messagebox
from models.student_model import StudentModel
from UI.styles import (
    BG_DARK, BG_CARD, BG_INPUT, ACCENT, BTN_GREY,
    TEXT_WHITE, TEXT_MUTED, FONT_TITLE, FONT_SUBTITLE,
    FONT_LABEL, FONT_ENTRY, FONT_BTN, ENTRY_W, PAD_Y
)


class StudentChangePassword:
    def __init__(self, root, prev_root):
        self.root      = root
        self.prev_root = prev_root
        self.model     = StudentModel()
        self.root.title("Student — Change Password")
        self.root.state("zoomed")
        self.root.configure(bg=BG_DARK)
        # self.root.resizable(True, True)
        self.root.protocol("WM_DELETE_WINDOW", self.go_back)
        self.build_ui()
        self.root.state('zoomed')

    def build_ui(self):
        outer = tk.Frame(self.root, bg=BG_DARK)
        outer.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(outer, text="CHANGE PASSWORD",
                 font=FONT_TITLE, bg=BG_DARK, fg=ACCENT).grid(row=0, column=0, pady=(0, 4))
        tk.Label(outer, text="Verify old_password password to set a new_password one",
                 font=FONT_SUBTITLE, bg=BG_DARK, fg=TEXT_MUTED).grid(row=1, column=0, pady=(0, 20))

        card = tk.Frame(outer, bg=BG_CARD, padx=50, pady=40)
        card.grid(row=2, column=0)

        self.student_id_var     = tk.StringVar()
        self.old_password_var     = tk.StringVar()
        self.new_password_var     = tk.StringVar()
        self.confirm_password_var = tk.StringVar()

        fields = [
            ("Student ID",       self.student_id_var,     False),
            ("Old Password",     self.old_password_var,     True),
            ("New Password",     self.new_password_var,     True),
            ("Confirm Password", self.confirm_password_var, True),
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
        tk.Button(card, text="UPDATE PASSWORD", bg=ACCENT,   fg=TEXT_WHITE, command=self.update,  **btn_cfg).grid(row=n*2,   column=0, sticky="ew", pady=(16, 6))
        tk.Button(card, text="⬅  BACK",         bg=BTN_GREY, fg=TEXT_WHITE, command=self.go_back, **btn_cfg).grid(row=n*2+1, column=0, sticky="ew")

    def update(self):
        try:
            student_id = int(self.student_id_var.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Student ID must be a number!", parent=self.root)
            return
        old_password     = self.old_password_var.get().strip()
        new_password     = self.new_password_var.get().strip()
        confirm_password = self.confirm_password_var.get().strip()
        if not all([old_password, new_password, confirm_password]):
            messagebox.showerror("Error", "All fields required!", parent=self.root)
            return
        if new_password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!", parent=self.root)
            return
        success = self.model.change_password(student_id, old_password, new_password)
        if success:
            messagebox.showinfo("Success", "Password changed!", parent=self.root)
            self.go_back()
        else:
            messagebox.showerror("Error", "Student ID or old_password Password incorrect!", parent=self.root)

    def go_back(self):
        self.root.destroy()
        self.prev_root.deiconify()
