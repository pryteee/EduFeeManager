# views/admin/add_counselor.py

import tkinter as tk
from tkinter import messagebox
from models.counselor_model import CounselorModel


from UI.styles import (
    BG_DARK, BG_CARD, BG_INPUT, ACCENT, BTN_GREY,
    TEXT_WHITE, TEXT_MUTED, FONT_TITLE, FONT_SUBTITLE,
    FONT_LABEL, FONT_ENTRY, FONT_BTN, ENTRY_W, PAD_Y,
    set_background, get_asset_path, place_on_canvas
)


class AddCounselor:
    def __init__(self, root, prev_root):
        self.root      = root
        self.prev_root = prev_root
        self.model     = CounselorModel()
        self.root.title("Admin — Add Counselor")
        self.root.state("zoomed")
        self.root.configure(bg="")
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

        tk.Label(outer, text="ADD COUNSELOR",
                font=FONT_TITLE, bg=BG_DARK, fg=ACCENT).grid(row=0, column=0, pady=(0, 4))
        tk.Label(outer, text="Fill in the details to add a new counselor",
                font=FONT_SUBTITLE, bg=BG_DARK, fg=TEXT_MUTED).grid(row=1, column=0, pady=(0, 20))

        card = tk.Frame(outer, bg=BG_CARD, padx=50, pady=40)
        card.grid(row=2, column=0)

        self.name_var    = tk.StringVar()
        self.email_id_var   = tk.StringVar()
        self.contact_var = tk.StringVar()
        self.username_var    = tk.StringVar()
        self.password_var    = tk.StringVar()

        fields = [
            ("Name",     self.name_var,    False),
            ("email_id",    self.email_id_var,   False),
            ("Contact",  self.contact_var, False),
            ("username", self.username_var,    False),
            ("password", self.password_var,    True),
        ]

        for i, (label, var, is_password) in enumerate(fields):
            tk.Label(card, text=label, font=FONT_LABEL,
                    bg=BG_CARD, fg=TEXT_WHITE, anchor="w"
                    ).grid(row=i*2, column=0, sticky="w", pady=(PAD_Y, 0))
            tk.Entry(card, textvariable=var, width=ENTRY_W,
                    show="*" if is_password else "",
                    font=FONT_ENTRY, bg=BG_INPUT, fg=TEXT_WHITE,
                    insertbackground=TEXT_WHITE, relief="flat", bd=6
                    ).grid(row=i*2+1, column=0, sticky="ew", pady=(0, PAD_Y))

        btn_cfg = dict(font=FONT_BTN, width=22, height=2, bd=0, cursor="hand2", relief="flat")
        n = len(fields)
        tk.Button(card, text="ADD COUNSELOR",
                bg=ACCENT, fg=TEXT_WHITE,
                command=self.add, **btn_cfg
                ).grid(row=n*2, column=0, sticky="ew", pady=(16, 6))
        tk.Button(card, text="⬅  BACK",
                bg=BTN_GREY, fg=TEXT_WHITE,
                command=self.go_back, **btn_cfg
                ).grid(row=n*2+1, column=0, sticky="ew")
        place_on_canvas(canvas, outer)

    def add(self):
        name    = self.name_var.get().strip()
        email_id   = self.email_id_var.get().strip()
        contact = self.contact_var.get().strip()
        username    = self.username_var.get().strip()
        password     = self.password_var.get().strip()
        if not all([name, email_id, contact, username, password]):
            messagebox.showerror("Error", "All fields required!", parent=self.root)
            return
        if self.model.username_exists(username):
            messagebox.showerror("Error", "username already exists!", parent=self.root)
            return
        if self.model.email_exists(email_id):
            messagebox.showerror("Error", "email_id already registered!", parent=self.root)
            return
        if self.model.contact_exists(contact):
            messagebox.showerror("Error", "Contact already registered!", parent=self.root)
            return
        success, c_id = self.model.register_counselor(name, email_id, contact, username, password)
        if success:
            messagebox.showinfo("Success", f"Counselor Added Successfully!\nCounselor ID = {c_id}", parent=self.root)
            self.go_back()
        else:
            messagebox.showerror("Error", "Failed to add counselor!", parent=self.root)

    def go_back(self):
        self.root.destroy()
        self.prev_root.deiconify()