import tkinter as tk
from models.fee_model import FeeModel
from UI.styles import (
    BG_DARK, BG_CARD, ACCENT, BTN_GREY,
    TEXT_WHITE, TEXT_MUTED, TEXT_SUCCESS, TEXT_WARN, TEXT_DANGER,
    FONT_TITLE, FONT_SUBTITLE, FONT_BTN, FONT_MONO,
    set_background, get_asset_path, place_on_canvas
)


class ViewPaymentStatus:
    def __init__(self, root, prev_root, student_data):
        self.root      = root
        self.prev_root = prev_root
        self.student   = student_data
        self.f_model   = FeeModel()
        self.root.title("Student — Payment Status")
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

        tk.Label(outer, text="PAYMENT STATUS",
                 font=FONT_TITLE, bg=BG_DARK, fg=ACCENT).grid(row=0, column=0, pady=(0, 4))
        tk.Label(outer, text="Your current fee payment summary",
                 font=FONT_SUBTITLE, bg=BG_DARK, fg=TEXT_MUTED).grid(row=1, column=0, pady=(0, 20))

        card = tk.Frame(outer, bg=BG_CARD, padx=50, pady=40)
        card.grid(row=2, column=0)

        fee = self.f_model.get_fee_with_student(self.student['student_id'])

        if fee:
            status_color = {
                "Fully Paid":   TEXT_SUCCESS,
                "Partial Paid": TEXT_WARN,
                "Pending":      TEXT_DANGER
            }.get(fee['status'], TEXT_WHITE)

            info_box = tk.Frame(card, bg="#0a1628", padx=24, pady=20)
            info_box.grid(row=0, column=0, sticky="ew", pady=(0, 16))

            rows = [
                ("Student ID",     str(fee['student_id']),       TEXT_WHITE),
                ("Name",           fee['name'],                  TEXT_WHITE),
                ("Course Fee",     f"₹{fee['course_fee']}",      TEXT_WHITE),
                ("Paid Amount",    f"₹{fee['paid_amount']}",     TEXT_SUCCESS),
                ("Pending Amount", f"₹{fee['pending_amount']}",  TEXT_WARN),
            ]
            for i, (label, value, color) in enumerate(rows):
                tk.Label(info_box, text=f"{label:<18}:", font=FONT_MONO,
                         bg="#0a1628", fg=TEXT_MUTED, anchor="w"
                         ).grid(row=i, column=0, sticky="w", pady=3)
                tk.Label(info_box, text=value, font=FONT_MONO,
                         bg="#0a1628", fg=color, anchor="w"
                         ).grid(row=i, column=1, sticky="w", padx=(8, 0), pady=3)

            # Status badge
            badge = tk.Frame(card, bg=BG_CARD)
            badge.grid(row=1, column=0, sticky="ew", pady=(0, 16))
            tk.Label(badge, text="Status :", font=FONT_MONO,
                     bg=BG_CARD, fg=TEXT_MUTED).pack(side="left")
            tk.Label(badge, text=f"  {fee['status']}",
                     font=("Helvetica", 14, "bold"),
                     bg=BG_CARD, fg=status_color).pack(side="left")
        else:
            tk.Label(card, text="No fee record found.\nContact your counselor.",
                     font=FONT_SUBTITLE, bg=BG_CARD, fg=TEXT_MUTED,
                     justify="center").grid(row=0, column=0, pady=30)

        tk.Button(card, text="⬅  BACK",
                  bg=BTN_GREY, fg=TEXT_WHITE,
                  font=FONT_BTN, width=22, height=2,
                  bd=0, cursor="hand2", relief="flat",
                  command=self.go_back).grid(row=3, column=0, sticky="ew")
        place_on_canvas(canvas, outer)

    def go_back(self):
        self.root.destroy()
        self.prev_root.deiconify()
