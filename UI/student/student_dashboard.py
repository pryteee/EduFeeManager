# UI/student/student_dashboard.py

import tkinter as tk
from UI.styles import (
    BG_DARK, BG_CARD, ACCENT, BTN_BLUE, BTN_GREY,
    TEXT_WHITE, TEXT_MUTED, FONT_TITLE, FONT_SUBTITLE, FONT_BTN,
    set_background, get_asset_path, place_on_canvas
)


class StudentDashboard:
    def __init__(self, root, prev_root, student_data):
        self.root      = root
        self.prev_root = prev_root
        self.student   = student_data
        self.root.title("Student — Dashboard")
        self.root.state("zoomed")
        self.root.configure(bg=BG_DARK)
        # self.root.resizable(True, True)
        self.root.protocol("WM_DELETE_WINDOW", self.logout)
        self.build_ui()
        self.root.state('zoomed')

    def build_ui(self):
        canvas = set_background(
            self.root,
            get_asset_path("student", "#image")
        )
        outer = tk.Frame(self.root, bg=BG_DARK)
        outer.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(outer, text="STUDENT DASHBOARD",
                 font=FONT_TITLE, bg=BG_DARK, fg=ACCENT).grid(row=0, column=0, pady=(0, 4))
        tk.Label(outer, text=f"Welcome, {self.student['name']}  |  ID: {self.student['student_id']}",
                 font=FONT_SUBTITLE, bg=BG_DARK, fg=TEXT_MUTED).grid(row=1, column=0, pady=(0, 30))

        card = tk.Frame(outer, bg=BG_CARD, padx=60, pady=40)
        card.grid(row=2, column=0)

        btn_cfg = dict(font=FONT_BTN, width=28, height=2, bd=0, cursor="hand2", relief="flat")

        tk.Button(card, text="📄   View Fee Details",
                  bg=BTN_BLUE, fg=TEXT_WHITE,
                  command=self.view_fee_details, **btn_cfg).grid(row=0, column=0, pady=8)

        tk.Button(card, text="💰   View Payment Status",
                  bg=BTN_BLUE, fg=TEXT_WHITE,
                  command=self.view_payment_status, **btn_cfg).grid(row=1, column=0, pady=8)

        tk.Button(card, text="🚪   Logout",
                  bg=BTN_GREY, fg=TEXT_WHITE,
                  command=self.logout, **btn_cfg).grid(row=2, column=0, pady=8)
        place_on_canvas(canvas, outer)
        

    def view_fee_details(self):
        from UI.student.view_fee_details import ViewFeeDetails
        self.root.withdraw()
        top = tk.Toplevel(self.root)
        ViewFeeDetails(top, self.root, self.student)

    def view_payment_status(self):
        from UI.student.view_payment_status import ViewPaymentStatus
        self.root.withdraw()
        top = tk.Toplevel(self.root)
        ViewPaymentStatus(top, self.root, self.student)

    def logout(self):
        self.root.destroy()
        self.prev_root.deiconify()