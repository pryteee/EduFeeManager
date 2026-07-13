import tkinter as tk
from tkinter import messagebox
import datetime
from models.student_model import StudentModel
from UI.styles import (
    BG_DARK, BG_CARD, BG_INPUT, ACCENT, BTN_GREY,
    TEXT_WHITE, TEXT_MUTED, FONT_TITLE, FONT_SUBTITLE,
    FONT_LABEL, FONT_ENTRY, FONT_BTN, ENTRY_W, PAD_Y,
    set_background, get_asset_path, place_on_canvas
)


class StudentRegister:
    def __init__(self, root, prev_root):
        self.root      = root
        self.prev_root = prev_root
        self.model     = StudentModel()
        self.root.title("Student — Registration")
        self.root.state("zoomed")
        self.root.configure(bg=BG_DARK)
        self.root.protocol("WM_DELETE_WINDOW", self.go_back)
        self.build_ui()

    def build_ui(self):
        canvas = set_background(
            self.root,
            get_asset_path("student", "#image")
        )
        outer = tk.Frame(self.root, bg=BG_DARK)
        outer.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(outer, text="STUDENT REGISTRATION",
                 font=FONT_TITLE, bg=BG_DARK,
                 fg=ACCENT).grid(row=0, column=0, pady=(0, 4))

        tk.Label(outer, text="Create your student account",
                 font=FONT_SUBTITLE, bg=BG_DARK,
                 fg=TEXT_MUTED).grid(row=1, column=0, pady=(0, 20))

        card = tk.Frame(outer, bg=BG_CARD, padx=50, pady=40)
        card.grid(row=2, column=0)

        self.name_var    = tk.StringVar()
        self.email_var   = tk.StringVar()
        self.contact_var = tk.StringVar()
        self.course_var  = tk.StringVar()
        self.user_var    = tk.StringVar()
        self.pass_var    = tk.StringVar()
        self.confirm_var = tk.StringVar()

        fields = [
            ("Full Name",        self.name_var,    False),
            ("Email",            self.email_var,   False),
            ("Contact Number",   self.contact_var, False),
            ("Course",           self.course_var,  False),
            ("Username",         self.user_var,    False),
            ("Password",         self.pass_var,    True),
            ("Confirm Password", self.confirm_var, True),
        ]

        for i, (label, var, is_pass) in enumerate(fields):
            tk.Label(card, text=label,
                     font=FONT_LABEL, bg=BG_CARD,
                     fg=TEXT_WHITE, anchor="w"
                     ).grid(row=i*2, column=0,
                            sticky="w", pady=(PAD_Y, 0))

            tk.Entry(card, textvariable=var,
                     width=ENTRY_W,
                     show="*" if is_pass else "",
                     font=FONT_ENTRY, bg=BG_INPUT,
                     fg=TEXT_WHITE,
                     insertbackground=TEXT_WHITE,
                     relief="flat", bd=6
                     ).grid(row=i*2+1, column=0,
                            sticky="ew", pady=(0, PAD_Y))

        n = len(fields)
        btn_cfg = dict(font=FONT_BTN, width=22, height=2,
                       bd=0, cursor="hand2", relief="flat")

        tk.Button(card, text="REGISTER",
                  bg=ACCENT, fg=TEXT_WHITE,
                  command=self.register,
                  **btn_cfg).grid(row=n*2, column=0,
                                  sticky="ew", pady=(16, 6))

        tk.Button(card, text="⬅  BACK",
                  bg=BTN_GREY, fg=TEXT_WHITE,
                  command=self.go_back,
                  **btn_cfg).grid(row=n*2+1, column=0,
                                  sticky="ew")
        place_on_canvas(canvas, outer)

    def register(self):
        
        name    = self.name_var.get().strip()
        email   = self.email_var.get().strip()
        contact = self.contact_var.get().strip()
        course  = self.course_var.get().strip()
        user    = self.user_var.get().strip()
        pwd     = self.pass_var.get().strip()
        confirm = self.confirm_var.get().strip()

        
        if not all([name, email, contact, course,
                    user, pwd, confirm]):
            messagebox.showerror("Error",
                                 "All fields are required!",
                                 parent=self.root)
            return

        
        if pwd != confirm:
            messagebox.showerror("Error",
                                 "Passwords do not match!",
                                 parent=self.root)
            return

        if len(pwd) < 4:
            messagebox.showerror("Error",
                                 "Password must be at least "
                                 "4 characters!",
                                 parent=self.root)
            return

        
        if self.model.username_exists(user):
            messagebox.showerror("Error",
                                 "Username already exists!",
                                 parent=self.root)
            return

        if self.model.email_exists(email):
            messagebox.showerror("Error",
                                 "Email already registered!",
                                 parent=self.root)
            return

        if self.model.contact_exists(contact):
            messagebox.showerror("Error",
                                 "Contact already registered!",
                                 parent=self.root)
            return

        
        year      = datetime.datetime.now().year
        total_fee = 0.00   # Counselor assigns fee later

        
        try:
            success, student_id = self.model.register_student(
                name,
                email,
                contact,
                course,
                user,
                pwd,
                year,
                total_fee
            )
        except Exception as e:
            messagebox.showerror("Database Error",
                                 f"Something went wrong:\n{e}",
                                 parent=self.root)
            return

        
        if success and student_id:
            messagebox.showinfo(
                "Registration Successful",
                f"Welcome, {name}!\n\n"
                f"Your Student ID is: {student_id}\n\n",
                # f" Save this ID — you need it to login!\n\n"
                # f"Fee details will be assigned\n"
                # f"by your counselor.",
                parent=self.root
            )
            self.go_back()
        else:
            messagebox.showerror(
                "Registration Failed",
                "Could not complete registration.\n"
                "Please check all details and try again.",
                parent=self.root
            )

    
    def go_back(self):
        self.root.destroy()
        self.prev_root.deiconify()
