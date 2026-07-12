import tkinter as tk
from tkinter import messagebox
from models.admin_model import AdminModel
from UI.styles import (
    BG_CARD, BG_INPUT, ACCENT, BTN_GREY, TEXT_WHITE, TEXT_MUTED,
    FONT_TITLE, FONT_SUBTITLE, FONT_LABEL, FONT_ENTRY, FONT_BTN,
    ENTRY_W, PAD_Y, set_background, get_asset_path, place_on_canvas
)


class AdminRegister:
    def __init__(self, root, prev_root):
        self.root      = root
        self.prev_root = prev_root
        self.model     = AdminModel()
        self.root.title("Admin — Registration")
        self.root.state("zoomed")
        self.root.resizable(True, True)
        self.root.protocol("WM_DELETE_WINDOW", self.go_back)
        self.build_ui()

    def build_ui(self):
        canvas = set_background(
            self.root,
            get_asset_path("admin", "#image")
        )

        outer = tk.Frame(canvas, bg=BG_CARD, padx=50, pady=40)

        tk.Label(outer, text="ADMIN REGISTRATION",
                 font=FONT_TITLE, bg=BG_CARD,
                 fg=ACCENT).grid(row=0, column=0, pady=(0, 4))
        tk.Label(outer, text="Create your admin account",
                 font=FONT_SUBTITLE, bg=BG_CARD,
                 fg=TEXT_MUTED).grid(row=1, column=0, pady=(0, 20))

        self.name_var    = tk.StringVar()
        self.username_var    = tk.StringVar()
        self.password_var    = tk.StringVar()
        self.email_id_var   = tk.StringVar()
        self.contact_var = tk.StringVar()

        fields = [
            ("Full Name",      self.name_var,    False),
            ("username",       self.username_var,    False),
            ("password",       self.password_var,    True),
            ("email ID",       self.email_id_var,   False),
            ("Contact Number", self.contact_var, False),
        ]

        for i, (label, var, is_password) in enumerate(fields):
            tk.Label(outer, text=label, font=FONT_LABEL,
                     bg=BG_CARD, fg=TEXT_WHITE,
                     anchor="w").grid(row=i*2+2, column=0,
                                      sticky="w", pady=(PAD_Y, 0))
            tk.Entry(outer, textvariable=var, width=ENTRY_W,
                     show="*" if is_password else "",
                     font=FONT_ENTRY, bg=BG_INPUT, fg=TEXT_WHITE,
                     insertbackground=TEXT_WHITE,
                     relief="flat", bd=6).grid(row=i*2+3, column=0,
                                               sticky="ew",
                                               pady=(0, PAD_Y))

        n = len(fields)
        btn_cfg = dict(font=FONT_BTN, width=22, height=2,
                       bd=0, cursor="hand2", relief="flat")

        tk.Button(outer, text="REGISTER",
                  bg=ACCENT, fg=TEXT_WHITE,
                  command=self.register,
                  **btn_cfg).grid(row=n*2+2, column=0,
                                  sticky="ew", pady=(16, 6))
        tk.Button(outer, text="⬅  BACK",
                  bg=BTN_GREY, fg=TEXT_WHITE,
                  command=self.go_back,
                  **btn_cfg).grid(row=n*2+3, column=0, sticky="ew")

        place_on_canvas(canvas, outer)

    def register(self):
        name    = self.name_var.get().strip()
        username    = self.username_var.get().strip()
        pwd     = self.password_var.get().strip()
        email_id   = self.email_id_var.get().strip()
        contact = self.contact_var.get().strip()
        if not all([name, username, pwd, email_id, contact]):
            messagebox.showerror("Error", "All fields are required!", parent=self.root)
            return
        if self.model.username_exists(username):
            messagebox.showerror("Error", "username already exists!", parent=self.root)
            return
        if self.model.email_id_exists(email_id):
            messagebox.showerror("Error", "email_id already registered!", parent=self.root)
            return
        if self.model.contact_exists(contact):
            messagebox.showerror("Error", "Contact already registered!", parent=self.root)
            return
        success, admin_id = self.model.register_admin(name, username, pwd, email_id, contact)
        if success:
            messagebox.showinfo("Success",
                                f"Registration Successful!\nYour Admin ID is: {admin_id}",
                                parent=self.root)
            self.go_back()
        else:
            messagebox.showerror("Error", "Registration failed.", parent=self.root)

    def go_back(self):
        self.root.destroy()
        self.prev_root.deiconify()