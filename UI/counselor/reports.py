# views/counselor/reports.py

import tkinter as tk
from tkinter import messagebox
from models.fee_model import FeeModel
from UI.styles import (
    BG_DARK, BG_CARD, BG_INPUT, ACCENT, BTN_BLUE, BTN_GREY,
    TEXT_WHITE, TEXT_MUTED, TEXT_SUCCESS, TEXT_WARN, TEXT_DANGER,
    FONT_TITLE, FONT_SUBTITLE, FONT_LABEL, FONT_BTN,
    set_background, get_asset_path, place_on_canvas
)


class Reports:
    def __init__(self, root, prev_root):
        self.root      = root
        self.prev_root = prev_root
        self.model     = FeeModel()
        self.root.title("Counselor — Reports")
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

        tk.Label(outer, text="FEE REPORTS",
                 font=FONT_TITLE, bg=BG_DARK, fg=ACCENT).grid(row=0, column=0, pady=(0, 4))
        tk.Label(outer, text="Summary of all student fee records",
                 font=FONT_SUBTITLE, bg=BG_DARK, fg=TEXT_MUTED).grid(row=1, column=0, pady=(0, 20))

        card = tk.Frame(outer, bg=BG_CARD, padx=60, pady=40)
        card.grid(row=2, column=0)

        self.report_items = [
            ("total_students",   "Total Students",        TEXT_WHITE),
            ("fully_paid",       "Fully Paid",            TEXT_SUCCESS),
            ("partial_paid",     "Partial Paid",          TEXT_WARN),
            ("pending",          "Pending",               TEXT_DANGER),
            ("total_collection", "Total Collection (₹)",  TEXT_SUCCESS),
            ("total_pending",    "Total Pending (₹)",     TEXT_DANGER),
        ]

        self.val_labels = {}
        for i, (key, display, color) in enumerate(self.report_items):
            row_frame = tk.Frame(card, bg="#0a1628", padx=16, pady=10)
            row_frame.grid(row=i, column=0, sticky="ew", pady=4)
            row_frame.columnconfigure(1, weight=1)

            tk.Label(row_frame, text=display,
                     font=FONT_LABEL, bg="#0a1628", fg=TEXT_MUTED,
                     width=24, anchor="w"
                     ).grid(row=0, column=0, sticky="w")

            val_lbl = tk.Label(row_frame, text="—",
                               font=("Helvetica", 13, "bold"),
                               bg="#0a1628", fg=color, anchor="e")
            val_lbl.grid(row=0, column=1, sticky="e")
            self.val_labels[key] = val_lbl

        btn_cfg = dict(font=FONT_BTN, width=22, height=2, bd=0, cursor="hand2", relief="flat")
        tk.Button(card, text="🔄  REFRESH",
                  bg=BTN_BLUE, fg=TEXT_WHITE,
                  command=self.load_reports, **btn_cfg
                  ).grid(row=len(self.report_items), column=0, sticky="ew", pady=(20, 6))
        tk.Button(card, text="⬅  BACK",
                  bg=BTN_GREY, fg=TEXT_WHITE,
                  command=self.go_back, **btn_cfg
                  ).grid(row=len(self.report_items)+1, column=0, sticky="ew")

        self.load_reports()
        place_on_canvas(canvas, outer)

    def load_reports(self):
        data = self.model.get_reports()
        if data:
            self.val_labels["total_students"].config(text=str(data['total_students'] or 0))
            self.val_labels["fully_paid"].config(text=str(data['fully_paid'] or 0))
            self.val_labels["partial_paid"].config(text=str(data['partial_paid'] or 0))
            self.val_labels["pending"].config(text=str(data['pending'] or 0))
            self.val_labels["total_collection"].config(text=f"₹{float(data['total_collection'] or 0):.2f}")
            self.val_labels["total_pending"].config(text=f"₹{float(data['total_pending'] or 0):.2f}")
        else:
            messagebox.showerror("Error", "Could not load reports!", parent=self.root)

    def go_back(self):
        self.root.destroy()
        self.prev_root.deiconify()