# views/student/view_fee_details.py

import tkinter as tk
from UI.styles import (
    BG_DARK, BG_CARD, ACCENT, BTN_GREY,
    TEXT_WHITE, TEXT_MUTED, FONT_TITLE, FONT_SUBTITLE,
    FONT_BTN, FONT_MONO,
    set_background, get_asset_path, place_on_canvas
)


class ViewFeeDetails:
    def __init__(self, root, prev_root, student_data):
        self.root      = root
        self.prev_root = prev_root
        self.student   = student_data
        self.root.title("Student — Fee Details")
        self.root.state("zoomed")
        self.root.configure(bg=BG_DARK)
        # self.root.resizable(True, True)
        self.root.protocol("WM_DELETE_WINDOW", self.go_back)
        self.build_ui()
        self.root.state('zoomed')

    def build_ui(self):
        canvas = set_background(
            self.root,
            get_asset_path("student", "#image")
        )
        outer = tk.Frame(self.root, bg=BG_DARK)
        outer.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(outer, text="FEE DETAILS",
                 font=FONT_TITLE, bg=BG_DARK, fg=ACCENT).grid(row=0, column=0, pady=(0, 4))
        tk.Label(outer, text="Your enrollment and course information",
                 font=FONT_SUBTITLE, bg=BG_DARK, fg=TEXT_MUTED).grid(row=1, column=0, pady=(0, 20))

        card = tk.Frame(outer, bg=BG_CARD, padx=50, pady=40)
        card.grid(row=2, column=0)

        info_box = tk.Frame(card, bg="#0a1628", padx=24, pady=20)
        info_box.grid(row=0, column=0, sticky="ew", pady=(0, 20))

        rows = [
            ("Student ID",    str(self.student['student_id'])),
            ("Name",          self.student['name']),
            ("Course",        self.student['course']),
            ("Academic Year", str(self.student['academic_year'])),
        ]
        for i, (label, value) in enumerate(rows):
            tk.Label(info_box, text=f"{label:<18}:", font=FONT_MONO,
                     bg="#0a1628", fg=TEXT_MUTED, anchor="w"
                     ).grid(row=i, column=0, sticky="w", pady=3)
            tk.Label(info_box, text=value, font=FONT_MONO,
                     bg="#0a1628", fg=TEXT_WHITE, anchor="w"
                     ).grid(row=i, column=1, sticky="w", padx=(8, 0), pady=3)

        tk.Button(card, text="⬅  BACK",
                  bg=BTN_GREY, fg=TEXT_WHITE,
                  font=FONT_BTN, width=22, height=2,
                  bd=0, cursor="hand2", relief="flat",
                  command=self.go_back).grid(row=1, column=0, sticky="ew")
        place_on_canvas(canvas, outer)

    def go_back(self):
        self.root.destroy()
        self.prev_root.deiconify()