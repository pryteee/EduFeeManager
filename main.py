import tkinter as tk
from UI.styles import (
    BG_DARK, BG_CARD, ACCENT, BTN_BLUE, BTN_GREY,
    TEXT_WHITE, TEXT_MUTED, FONT_TITLE, FONT_SUBTITLE, FONT_BTN
)


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Fee Structure Management System")
        self.root.state("zoomed")
        self.root.configure(bg="#f8f8f8")
        self.root.resizable(True, True)
        self.build_ui()

    def build_ui(self):
        outer = tk.Frame(self.root, bg="#f8f8f8")
        outer.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            outer,
            text="FEE STRUCTURE\nMANAGEMENT SYSTEM",
            font=FONT_TITLE,
            bg="#f8f8f8",          
            fg=ACCENT,
            justify="center"
        ).grid(row=0, column=0, pady=(0, 6))

        tk.Label(
            outer,
            text="Select your role to continue",
            font=FONT_SUBTITLE,
            bg="#f8f8f8",          
            fg=TEXT_MUTED
        ).grid(row=1, column=0, pady=(0, 30))

        
        card = tk.Frame(outer, bg="#f8f8f8", padx=60, pady=40)
        card.grid(row=2, column=0)

        btn_cfg = dict(
            font=FONT_BTN, width=26, height=2,
            bd=0, cursor="hand2", relief="flat"
        )

        tk.Button(card, text="👤   ADMIN",
                  bg=ACCENT, fg=TEXT_WHITE,
                  command=self.open_admin, **btn_cfg).grid(row=0, column=0, pady=8)

        tk.Button(card, text="🧑‍💼   COUNSELOR",
                  bg=BTN_BLUE, fg=TEXT_WHITE,
                  command=self.open_counselor, **btn_cfg).grid(row=1, column=0, pady=8)

        tk.Button(card, text="🎓   STUDENT",
                  bg=BTN_BLUE, fg=TEXT_WHITE,
                  command=self.open_student, **btn_cfg).grid(row=2, column=0, pady=8)

        tk.Button(card, text="❌   EXIT",
                  bg=BTN_GREY, fg=TEXT_WHITE,
                  command=self.root.destroy, **btn_cfg).grid(row=3, column=0, pady=8)

    def open_admin(self):
        from UI.admin.admin_home import AdminHome
        self.root.withdraw()
        top = tk.Toplevel(self.root)
        AdminHome(top, self.root)

    def open_counselor(self):
        from UI.counselor.counselor_home import CounselorHome
        self.root.withdraw()
        top = tk.Toplevel(self.root)
        CounselorHome(top, self.root)

    def open_student(self):
        from UI.student.student_home import StudentHome
        self.root.withdraw()
        top = tk.Toplevel(self.root)
        StudentHome(top, self.root)


if __name__ == "__main__":
    from UI.welcome_page import WelcomePage
    root = tk.Tk()
    WelcomePage(root)
    root.mainloop()