import tkinter as tk
from tkinter import messagebox
from models.counselor_model import CounselorModel
from UI.styles import (
    BG_DARK, BG_CARD, BG_INPUT, ACCENT, BTN_BLUE, BTN_GREY,
    TEXT_WHITE, TEXT_MUTED, FONT_TITLE, FONT_SUBTITLE,
    FONT_LABEL, FONT_ENTRY, FONT_BTN, ENTRY_W, PAD_Y,
    ENTRY_W, PAD_Y, set_background, get_asset_path, place_on_canvas
)


class EditCounselor:
    def __init__(self, root, prev_root):
        self.root      = root
        self.prev_root = prev_root
        self.model     = CounselorModel()
        self.root.title("Admin — Edit Counselor")
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

        tk.Label(outer, text="EDIT COUNSELOR",
                 font=FONT_TITLE, bg=BG_DARK, fg=ACCENT).grid(row=0, column=0, pady=(0, 4))
        tk.Label(outer, text="Search by ID then update details",
                 font=FONT_SUBTITLE, bg=BG_DARK, fg=TEXT_MUTED).grid(row=1, column=0, pady=(0, 20))

        card = tk.Frame(outer, bg=BG_CARD, padx=50, pady=40)
        card.grid(row=2, column=0)

        self.cid_var     = tk.StringVar()
        self.name_var    = tk.StringVar()
        self.email_var   = tk.StringVar()
        self.contact_var = tk.StringVar()
        self.user_var    = tk.StringVar()
        self.pass_var    = tk.StringVar()

        btn_cfg   = dict(font=FONT_BTN, height=2, bd=0, cursor="hand2", relief="flat")
        entry_cfg = dict(font=FONT_ENTRY, bg=BG_INPUT, fg=TEXT_WHITE,
                         insertbackground=TEXT_WHITE, relief="flat", bd=6)

        # Search row
        tk.Label(card, text="Counselor ID", font=FONT_LABEL,
                 bg=BG_CARD, fg=TEXT_WHITE, anchor="w"
                 ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 4))

        search_frame = tk.Frame(card, bg=BG_CARD)
        search_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 14))

        tk.Entry(search_frame, textvariable=self.cid_var, width=20,
                 **entry_cfg).pack(side="left", padx=(0, 8))
        tk.Button(search_frame, text="SEARCH", bg=BTN_BLUE, fg=TEXT_WHITE,
                  width=10, **btn_cfg, command=self.search).pack(side="left")

        # Editable fields
        fields = [
            ("Name",     self.name_var,    False),
            ("Email",    self.email_var,   False),
            ("Contact",  self.contact_var, False),
            ("Username", self.user_var,    False),
            ("Password", self.pass_var,    True),
        ]
        for i, (label, var, is_pass) in enumerate(fields):
            tk.Label(card, text=label, font=FONT_LABEL,
                     bg=BG_CARD, fg=TEXT_WHITE, anchor="w"
                     ).grid(row=(i+1)*2, column=0, columnspan=2, sticky="w", pady=(PAD_Y, 0))
            tk.Entry(card, textvariable=var, width=ENTRY_W,
                     show="*" if is_pass else "", **entry_cfg
                     ).grid(row=(i+1)*2+1, column=0, columnspan=2, sticky="ew", pady=(0, PAD_Y))

        n = len(fields)
        tk.Button(card, text="UPDATE",
                  bg=ACCENT, fg=TEXT_WHITE, width=22,
                  command=self.update, **btn_cfg
                  ).grid(row=(n+1)*2, column=0, columnspan=2, sticky="ew", pady=(16, 6))
        tk.Button(card, text="⬅  BACK",
                  bg=BTN_GREY, fg=TEXT_WHITE, width=22,
                  command=self.go_back, **btn_cfg
                  ).grid(row=(n+1)*2+1, column=0, columnspan=2, sticky="ew")
        place_on_canvas(canvas, outer)

    def search(self):
        try:
            cid = int(self.cid_var.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Enter valid Counselor ID!", parent=self.root)
            return
        data = self.model.get_counselor_by_id(cid)
        if data:
            self.name_var.set(data['name'])
            self.email_var.set(data['email'])
            self.contact_var.set(data['contact'])
            self.user_var.set(data['username'])
            self.pass_var.set(data['password'])
        else:
            messagebox.showerror("Error", "Counselor not found!", parent=self.root)

    def update(self):
        try:
            cid = int(self.cid_var.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Search a counselor first!", parent=self.root)
            return
        name    = self.name_var.get().strip()
        email   = self.email_var.get().strip()
        contact = self.contact_var.get().strip()
        user    = self.user_var.get().strip()
        pwd     = self.pass_var.get().strip()
        if not all([name, email, contact, user, pwd]):
            messagebox.showerror("Error", "All fields required!", parent=self.root)
            return
        success = self.model.update_counselor(cid, name, email, contact, user, pwd)
        if success:
            messagebox.showinfo("Success", "Counselor updated successfully!", parent=self.root)
            self.go_back()
        else:
            messagebox.showerror("Error", "Update failed!", parent=self.root)

    def go_back(self):
        self.root.destroy()
        self.prev_root.deiconify()
