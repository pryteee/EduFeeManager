import tkinter as tk
from tkinter import messagebox
from models.counselor_model import CounselorModel
from UI.styles import (
    BG_DARK, BG_CARD, BG_INPUT, ACCENT, BTN_BLUE, BTN_GREY,
    TEXT_WHITE, TEXT_MUTED, FONT_TITLE, FONT_SUBTITLE,
    FONT_LABEL, FONT_ENTRY, FONT_BTN, ENTRY_W, PAD_Y,
    ENTRY_W, PAD_Y, set_background, get_asset_path, place_on_canvas
)


class DeleteCounselor:
    def __init__(self, root, prev_root):
        self.root      = root
        self.prev_root = prev_root
        self.model     = CounselorModel()
        self.found     = None
        self.root.title("Admin — Delete Counselor")
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

        tk.Label(outer, text="DELETE COUNSELOR",
                 font=FONT_TITLE, bg=BG_DARK, fg=ACCENT).grid(row=0, column=0, pady=(0, 4))
        tk.Label(outer, text="Search counselor then confirm deletion",
                 font=FONT_SUBTITLE, bg=BG_DARK, fg=TEXT_MUTED).grid(row=1, column=0, pady=(0, 20))

        card = tk.Frame(outer, bg=BG_CARD, padx=50, pady=40)
        card.grid(row=2, column=0)

        self.cid_var = tk.StringVar()
        btn_cfg = dict(font=FONT_BTN, height=2, bd=0, cursor="hand2", relief="flat")

        tk.Label(card, text="Counselor ID", font=FONT_LABEL,
                 bg=BG_CARD, fg=TEXT_WHITE, anchor="w"
                 ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 4))

        sf = tk.Frame(card, bg=BG_CARD)
        sf.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 16))
        tk.Entry(sf, textvariable=self.cid_var, width=22,
                 font=FONT_ENTRY, bg=BG_INPUT, fg=TEXT_WHITE,
                 insertbackground=TEXT_WHITE, relief="flat", bd=6
                 ).pack(side="left", padx=(0, 8))
        tk.Button(sf, text="SEARCH", bg=BTN_BLUE, fg=TEXT_WHITE,
                  width=10, **btn_cfg, command=self.search).pack(side="left")

        # Info display box
        self.info_frame = tk.Frame(card, bg="#0a1628", padx=16, pady=12)
        self.info_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 16))

        self.info_label = tk.Label(
            self.info_frame, text="No record loaded.",
            font=("Courier", 11), bg="#0a1628", fg=TEXT_MUTED,
            justify="left", anchor="w"
        )
        self.info_label.pack(fill="x")

        tk.Button(card, text="🗑️  DELETE COUNSELOR",
                  bg=ACCENT, fg=TEXT_WHITE, width=22,
                  command=self.delete, **btn_cfg
                  ).grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 6))

        tk.Button(card, text="⬅  BACK",
                  bg=BTN_GREY, fg=TEXT_WHITE, width=22,
                  command=self.go_back, **btn_cfg
                  ).grid(row=4, column=0, columnspan=2, sticky="ew")
        place_on_canvas(canvas, outer)

    def search(self):
        try:
            cid = int(self.cid_var.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Enter valid Counselor ID!", parent=self.root)
            return
        self.found = self.model.get_counselor_by_id(cid)
        if self.found:
            self.info_label.config(
                fg=TEXT_WHITE,
                text=(f"  ID       : {self.found['counselor_id']}\n"
                      f"  Name     : {self.found['name']}\n"
                      f"  Email    : {self.found['email']}\n"
                      f"  Contact  : {self.found['contact']}\n"
                      f"  Username : {self.found['username']}")
            )
        else:
            self.info_label.config(text="No record loaded.", fg=TEXT_MUTED)
            messagebox.showerror("Error", "Counselor not found!", parent=self.root)

    def delete(self):
        if not self.found:
            messagebox.showerror("Error", "Search a counselor first!", parent=self.root)
            return
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete '{self.found['name']}'?\nThis action cannot be undone.",
            parent=self.root
        )
        if confirm:
            success = self.model.delete_counselor(self.found['counselor_id'])
            if success:
                messagebox.showinfo("Deleted", "Counselor deleted successfully!", parent=self.root)
                self.found = None
                self.info_label.config(text="No record loaded.", fg=TEXT_MUTED)
                self.cid_var.set("")
            else:
                messagebox.showerror("Error", "Deletion failed!", parent=self.root)

    def go_back(self):
        self.root.destroy()
        self.prev_root.deiconify()
