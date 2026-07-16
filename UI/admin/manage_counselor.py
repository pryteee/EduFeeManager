import tkinter as tk
from UI.styles import (
    BG_CARD, ACCENT, BTN_BLUE, BTN_GREY,
    TEXT_WHITE, TEXT_MUTED, FONT_TITLE, FONT_SUBTITLE, FONT_BTN,
    set_background, get_asset_path, place_on_canvas
)


class ManageCounselor:
    def __init__(self, root, prev_root, admin_data):
        self.root      = root
        self.prev_root = prev_root
        self.admin     = admin_data
        self.root.title("Admin — Manage Counselors")
        self.root.state("zoomed")
        self.root.resizable(True, True)
        self.root.protocol("WM_DELETE_WINDOW", self.logout)
        self.build_ui()

    def build_ui(self):
        canvas = set_background(
            self.root,
            get_asset_path("admin", "#image")
        )

        outer = tk.Frame(canvas, bg=BG_CARD, padx=50, pady=40)

        tk.Label(outer, text="MANAGE COUNSELORS",
                 font=FONT_TITLE, bg=BG_CARD,
                 fg=ACCENT).grid(row=0, column=0, columnspan=2, pady=(0, 4))
        tk.Label(outer, text=f"Logged in as: {self.admin['name']}",
                 font=FONT_SUBTITLE, bg=BG_CARD,
                 fg=TEXT_MUTED).grid(row=1, column=0, columnspan=2, pady=(0, 24))

        btn_cfg = dict(font=FONT_BTN, width=24, height=2,
                       bd=0, cursor="hand2", relief="flat")

        buttons = [
            ("  Add Counselor",       BTN_BLUE, self.add_counselor,   0, 0),
            ("  Edit Counselor",      BTN_BLUE, self.edit_counselor,  0, 1),
            ("  Delete Counselor",   BTN_BLUE, self.delete_counselor, 1, 0),
            ("  View Counselor",     BTN_BLUE, self.view_counselor,   1, 1),
            ("  View All Counselors", BTN_BLUE, self.view_all,         2, 0),
            ("  Delete Student",     ACCENT,   self.delete_student,   2, 1),
        ]
        for text, color, cmd, row, col in buttons:
            tk.Button(outer, text=text, bg=color, fg=TEXT_WHITE,
                      command=cmd,
                      **btn_cfg).grid(row=row+2, column=col,
                                      padx=8, pady=8, sticky="ew")

        tk.Button(outer, text="🚪  Logout",
                  bg=BTN_GREY, fg=TEXT_WHITE,
                  command=self.logout,
                  **btn_cfg).grid(row=5, column=0, columnspan=2,
                                  pady=(8, 0), sticky="ew")

        place_on_canvas(canvas, outer)

    def add_counselor(self):
        from UI.admin.add_counselor import AddCounselor
        self.root.withdraw()
        top = tk.Toplevel(self.root)
        AddCounselor(top, self.root)

    def edit_counselor(self):
        from UI.admin.edit_counselor import EditCounselor
        self.root.withdraw()
        top = tk.Toplevel(self.root)
        EditCounselor(top, self.root)

    def delete_counselor(self):
        from UI.admin.delete_counselor import DeleteCounselor
        self.root.withdraw()
        top = tk.Toplevel(self.root)
        DeleteCounselor(top, self.root)

    def view_counselor(self):
        from UI.admin.view_counselor import ViewCounselor
        self.root.withdraw()
        top = tk.Toplevel(self.root)
        ViewCounselor(top, self.root)

    def view_all(self):
        from UI.admin.view_all_counselors import ViewAllCounselors
        self.root.withdraw()
        top = tk.Toplevel(self.root)
        ViewAllCounselors(top, self.root)

    def delete_student(self):
        from UI.admin.delete_student import DeleteStudent
        self.root.withdraw()
        top = tk.Toplevel(self.root)
        DeleteStudent(top, self.root)

    def logout(self):
        self.root.destroy()
        self.prev_root.deiconify()
