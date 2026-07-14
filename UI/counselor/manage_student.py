import tkinter as tk
from UI.styles import (
    BG_DARK, BG_CARD, ACCENT, BTN_BLUE, BTN_GREY,
    TEXT_WHITE, TEXT_MUTED, FONT_TITLE, FONT_SUBTITLE, FONT_BTN,
    set_background, get_asset_path, place_on_canvas
)


class ManageStudent:
    def __init__(self, root, prev_root, counselor_data):
        self.root      = root
        self.prev_root = prev_root
        self.counselor = counselor_data
        self.root.title("Counselor — Manage Students")
        self.root.state("zoomed")
        self.root.configure(bg=BG_DARK)
        # self.root.resizable(True, True)
        self.root.protocol("WM_DELETE_WINDOW", self.logout)
        self.build_ui()
        self.root.state('zoomed')

    def build_ui(self):
        canvas = set_background(
            self.root,
            get_asset_path("counselor", "#image")
        )
        outer = tk.Frame(self.root, bg=BG_DARK)
        outer.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(outer, text="MANAGE STUDENTS",
                 font=FONT_TITLE, bg=BG_DARK, fg=ACCENT).grid(row=0, column=0, columnspan=2, pady=(0, 4))
        tk.Label(outer, text=f"Logged in as: {self.counselor['name']}",
                 font=FONT_SUBTITLE, bg=BG_DARK, fg=TEXT_MUTED).grid(row=1, column=0, columnspan=2, pady=(0, 24))

        card = tk.Frame(outer, bg=BG_CARD, padx=50, pady=40)
        card.grid(row=2, column=0, columnspan=2)

        btn_cfg = dict(font=FONT_BTN, width=24, height=2, bd=0, cursor="hand2", relief="flat")

        buttons = [
            ("  Add Student",         BTN_BLUE, self.add_student,    0, 0),
            ("  Update Student",      BTN_BLUE, self.update_student, 0, 1),
            ("  View Fee Structure", BTN_BLUE, self.view_fee,       1, 0),
            ("  Edit Fee Structure", BTN_BLUE, self.edit_fee,       1, 1),
            ("  Reports",             BTN_BLUE, self.reports,        2, 0),
            ("  Detailed Report",    BTN_BLUE, self.detailed_report, 2, 1),
        ]
        for text, color, cmd, row, col in buttons:
            tk.Button(card, text=text, bg=color, fg=TEXT_WHITE,
                      command=cmd, **btn_cfg
                      ).grid(row=row, column=col, padx=8, pady=8, sticky="ew")

        tk.Button(card, text="🚪  Logout",
                  bg=BTN_GREY, fg=TEXT_WHITE, command=self.logout, **btn_cfg
                  ).grid(row=3, column=0, columnspan=2, pady=(8, 0), sticky="ew")
        place_on_canvas(canvas, outer)
    def add_student(self):
        from UI.counselor.add_student import AddStudent
        self.root.withdraw()
        top = tk.Toplevel(self.root)
        AddStudent(top, self.root, self.counselor['counselor_id'])
    
    def detailed_report(self):
        from UI.counselor.detailed_report import DetailedReport
        self.root.withdraw()
        top = tk.Toplevel(self.root)
        DetailedReport(top, self.root)

    def update_student(self):
        from UI.counselor.update_student import UpdateStudent
        self.root.withdraw()
        top = tk.Toplevel(self.root)
        UpdateStudent(top, self.root, self.counselor['counselor_id'])

    def view_fee(self):
        from UI.counselor.view_fee_structure import ViewFeeStructure
        self.root.withdraw()
        top = tk.Toplevel(self.root)
        ViewFeeStructure(top, self.root)

    def edit_fee(self):
        from UI.counselor.edit_fee_structure import EditFeeStructure
        self.root.withdraw()
        top = tk.Toplevel(self.root)
        EditFeeStructure(top, self.root)

    def reports(self):
        from UI.counselor.reports import Reports
        self.root.withdraw()
        top = tk.Toplevel(self.root)
        Reports(top, self.root)

    def logout(self):
        self.root.destroy()
        self.prev_root.deiconify()
    
