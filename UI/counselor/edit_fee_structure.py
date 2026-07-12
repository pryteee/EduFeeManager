# views/counselor/edit_fee_structure.py

import tkinter as tk
from tkinter import messagebox
from models.fee_model import FeeModel
from UI.styles import (
    BG_DARK, BG_CARD, BG_INPUT, ACCENT, BTN_BLUE, BTN_GREY,
    TEXT_WHITE, TEXT_MUTED, FONT_TITLE, FONT_SUBTITLE,
    FONT_LABEL, FONT_ENTRY, FONT_BTN, ENTRY_W, PAD_Y,
    set_background, get_asset_path, place_on_canvas
)


class EditFeeStructure:
    def __init__(self, root, prev_root):
        self.root      = root
        self.prev_root = prev_root
        self.model     = FeeModel()
        self.root.title("Counselor — Edit Fee Structure")
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

        tk.Label(outer, text="EDIT FEE STRUCTURE",
                 font=FONT_TITLE, bg=BG_DARK, fg=ACCENT).grid(row=0, column=0, pady=(0, 4))
        tk.Label(outer, text="Search then edit paid_amount and pending_amount amounts",
                 font=FONT_SUBTITLE, bg=BG_DARK, fg=TEXT_MUTED).grid(row=1, column=0, pady=(0, 20))

        card = tk.Frame(outer, bg=BG_CARD, padx=50, pady=40)
        card.grid(row=2, column=0)

        self.student_id_var     = tk.StringVar()
        self.name_var    = tk.StringVar()
        self.course_var  = tk.StringVar()
        self.fee_var     = tk.StringVar()
        self.paid_amount_var    = tk.StringVar()
        self.pending_amount_var = tk.StringVar()
        self.status_var  = tk.StringVar()

        entry_cfg  = dict(font=FONT_ENTRY, bg=BG_INPUT, fg=TEXT_WHITE,
                          insertbackground=TEXT_WHITE, relief="flat", bd=6)
        ro_cfg     = dict(font=FONT_ENTRY, state="readonly",
                          readonlybackground="#0a1628", fg=TEXT_MUTED,
                          relief="flat", bd=6)
        btn_cfg    = dict(font=FONT_BTN, height=2, bd=0, cursor="hand2", relief="flat")

        
        tk.Label(card, text="Student ID", font=FONT_LABEL,
                 bg=BG_CARD, fg=TEXT_WHITE, anchor="w"
                 ).grid(row=0, column=0, sticky="w", pady=(0, 4))
        sf = tk.Frame(card, bg=BG_CARD)
        sf.grid(row=1, column=0, sticky="ew", pady=(0, 16))
        tk.Entry(sf, textvariable=self.student_id_var, width=22, **entry_cfg)\
            .pack(side="left", padx=(0, 8))

        tk.Button(sf, text="SEARCH", bg=BTN_BLUE, fg=TEXT_WHITE,
                width=10, **btn_cfg, command=self.search)\
            .pack(side="left")

        
        for i, (label, var) in enumerate([("Student Name", self.name_var), ("Course", self.course_var)]):
            tk.Label(card, text=f"{label} (read-only)", font=FONT_LABEL,
                     bg=BG_CARD, fg=TEXT_MUTED, anchor="w"
                     ).grid(row=i*2+2, column=0, sticky="w", pady=(PAD_Y, 0))
            tk.Entry(card, textvariable=var, width=ENTRY_W, **ro_cfg
                     ).grid(row=i*2+3, column=0, sticky="ew", pady=(0, PAD_Y))

        
        editable = [
            ("Course Fee",     self.fee_var),
            ("paid Amount",    self.paid_amount_var),
            ("pending Amount", self.pending_amount_var),
        ]
        for i, (label, var) in enumerate(editable):
            tk.Label(card, text=label, font=FONT_LABEL,
                     bg=BG_CARD, fg=TEXT_WHITE, anchor="w"
                     ).grid(row=i*2+6, column=0, sticky="w", pady=(PAD_Y, 0))
            tk.Entry(card, textvariable=var, width=ENTRY_W, **entry_cfg
                     ).grid(row=i*2+7, column=0, sticky="ew", pady=(0, PAD_Y))

        tk.Label(card, text="Status (auto-calculated)", font=FONT_LABEL,
                 bg=BG_CARD, fg=TEXT_MUTED, anchor="w"
                 ).grid(row=12, column=0, sticky="w", pady=(PAD_Y, 0))
        tk.Entry(card, textvariable=self.status_var, width=ENTRY_W, **ro_cfg
                 ).grid(row=13, column=0, sticky="ew", pady=(0, PAD_Y))

        tk.Button(card, text="UPDATE FEE", bg=ACCENT,   fg=TEXT_WHITE, width=22, command=self.update,  **btn_cfg).grid(row=14, column=0, sticky="ew", pady=(16, 6))
        tk.Button(card, text="⬅  BACK",    bg=BTN_GREY, fg=TEXT_WHITE, width=22, command=self.go_back, **btn_cfg).grid(row=15, column=0, sticky="ew")
        place_on_canvas(canvas, outer)
    def search(self):
        try:
            student_id = int(self.student_id_var.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Enter valid Student ID!", parent=self.root)
            return
        data = self.model.get_fee_with_student(student_id)
        if data:
            self.name_var.set(data['name'])
            self.course_var.set(data['course'])
            self.fee_var.set(data['course_fee'])
            self.paid_amount_var.set(data['paid_amount'])
            self.pending_amount_var.set(data['pending_amount'])
            self.status_var.set(data['status'])
        else:
            messagebox.showerror("Error", "Record not found!", parent=self.root)

    def update(self):
        try:
            student_id  = int(self.student_id_var.get().strip())
            fee         = float(self.fee_var.get().strip())
            paid_amount = float(self.paid_amount_var.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Enter valid numeric values!", parent=self.root)
            return

        pending_amount = round(fee - paid_amount, 2)
        status = self.model.calculate_status(paid_amount, pending_amount)

        self.pending_amount_var.set(pending_amount)
        self.status_var.set(status)

        success = self.model.update_fee(
            student_id, fee, paid_amount, pending_amount, status
        )

        if success:
            messagebox.showinfo("Success", f"Fee updated!\nStatus: {status}", parent=self.root)
            self.go_back()
        else:
            messagebox.showerror("Error", "Update failed!", parent=self.root)

    def go_back(self):
        self.root.destroy()
        self.prev_root.deiconify()