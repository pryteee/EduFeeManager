# views/counselor/view_fee_structure.py

import tkinter as tk
from tkinter import messagebox
from models.fee_model import FeeModel
from UI.styles import (
    BG_DARK, BG_CARD, BG_INPUT, ACCENT, BTN_BLUE, BTN_GREY,
    TEXT_WHITE, TEXT_MUTED, FONT_TITLE, FONT_SUBTITLE,
    FONT_LABEL, FONT_ENTRY, FONT_BTN, FONT_MONO, PAD_Y,
    set_background, get_asset_path, place_on_canvas
)


class ViewFeeStructure:
    def __init__(self, root, prev_root):
        self.root      = root
        self.prev_root = prev_root
        self.model     = FeeModel()
        self.root.title("Counselor — View Fee Structure")
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

        tk.Label(outer, text="VIEW FEE STRUCTURE",
                 font=FONT_TITLE, bg=BG_DARK, fg=ACCENT).grid(row=0, column=0, pady=(0, 4))
        tk.Label(outer, text="Enter Student ID to view fee details",
                 font=FONT_SUBTITLE, bg=BG_DARK, fg=TEXT_MUTED).grid(row=1, column=0, pady=(0, 20))

        card = tk.Frame(outer, bg=BG_CARD, padx=50, pady=40)
        card.grid(row=2, column=0)

        self.sid_var = tk.StringVar()
        btn_cfg = dict(font=FONT_BTN, height=2, bd=0, cursor="hand2", relief="flat")

        tk.Label(card, text="Student ID", font=FONT_LABEL,
                 bg=BG_CARD, fg=TEXT_WHITE, anchor="w"
                 ).grid(row=0, column=0, sticky="w", pady=(0, 4))

        sf = tk.Frame(card, bg=BG_CARD)
        sf.grid(row=1, column=0, sticky="ew", pady=(0, 16))
        tk.Entry(sf, textvariable=self.sid_var, width=22,
                 font=FONT_ENTRY, bg=BG_INPUT, fg=TEXT_WHITE,
                 insertbackground=TEXT_WHITE, relief="flat", bd=6
                 ).pack(side="left", padx=(0, 8))
        tk.Button(sf, text="SEARCH", bg=BTN_BLUE, fg=TEXT_WHITE,
                  width=10, **btn_cfg, command=self.search).pack(side="left")

        info_box = tk.Frame(card, bg="#0a1628", padx=20, pady=16)
        info_box.grid(row=2, column=0, sticky="ew", pady=(0, 16))
        self.info = tk.Label(info_box, text="No record loaded.",
                             font=FONT_MONO, bg="#0a1628", fg=TEXT_MUTED,
                             justify="left", anchor="w")
        self.info.pack(fill="x")

        tk.Button(card, text="⬅  BACK",
                  bg=BTN_GREY, fg=TEXT_WHITE, width=22,
                  command=self.go_back, **btn_cfg
                  ).grid(row=3, column=0, sticky="ew")
        place_on_canvas(canvas, outer)
    def search(self):
        try:
            sid = int(self.sid_var.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Enter valid Student ID!", parent=self.root)
            return
        data = self.model.get_fee_with_student(sid)
        if data:
            self.info.config(fg=TEXT_WHITE, text=(
                f"  Student ID     : {data['student_id']}\n"
                f"  Name           : {data['name']}\n"
                f"  Course         : {data['course']}\n"
                f"  Course Fee     : ₹{data['course_fee']}\n"
                f"  Paid Amount    : ₹{data['paid_amount']}\n"
                f"  Pending Amount : ₹{data['pending_amount']}\n"
                f"  Status         : {data['status']}"
            ))
        else:
            self.info.config(text="No record loaded.", fg=TEXT_MUTED)
            messagebox.showerror("Error", "Student or fee record not found!", parent=self.root)

    def go_back(self):
        self.root.destroy()
        self.prev_root.deiconify()