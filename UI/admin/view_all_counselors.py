import tkinter as tk
from tkinter import ttk
from models.counselor_model import CounselorModel
from UI.styles import (
    BG_DARK, BG_CARD, BG_INPUT, ACCENT, BTN_GREY,
    TEXT_WHITE, TEXT_MUTED, FONT_TITLE, FONT_SUBTITLE, FONT_BTN
)


class ViewAllCounselors:
    def __init__(self, root, prev_root):
        self.root      = root
        self.prev_root = prev_root
        self.model     = CounselorModel()
        self.root.title("Admin — All Counselors")
        self.root.state("zoomed")
        self.root.configure(bg=BG_DARK)
        # self.root.resizable(True, True)
        self.root.protocol("WM_DELETE_WINDOW", self.go_back)
        self.build_ui()
        self.root.state('zoomed')

    def build_ui(self):
        
        header = tk.Frame(self.root, bg=BG_DARK, pady=20)
        header.pack(fill="x")
        tk.Label(header, text="ALL COUNSELORS",
                 font=FONT_TITLE, bg=BG_DARK, fg=ACCENT).pack()
        tk.Label(header, text="Complete list of registered counselors",
                 font=FONT_SUBTITLE, bg=BG_DARK, fg=TEXT_MUTED).pack()

        tree_frame = tk.Frame(self.root, bg=BG_DARK, padx=30, pady=10)
        tree_frame.pack(fill="both", expand=True)

        cols = ("ID", "Name", "Email", "Contact", "Username", "Joined")
        self.tree = ttk.Treeview(tree_frame, columns=cols, show="headings")

        col_widths = {"ID": 60, "Name": 180, "Email": 220,
                      "Contact": 130, "Username": 140, "Joined": 170}
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=col_widths[col], anchor="center", minwidth=60)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background=BG_CARD, fieldbackground=BG_CARD,
                        foreground=TEXT_WHITE, rowheight=30,
                        font=("Helvetica", 11))
        style.configure("Treeview.Heading",
                        background="#0f3460", foreground=TEXT_WHITE,
                        font=("Helvetica", 11, "bold"))
        style.map("Treeview", background=[("selected", ACCENT)])

        vsb = ttk.Scrollbar(tree_frame, orient="vertical",   command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)

        self.load_data()

        
        footer = tk.Frame(self.root, bg=BG_DARK, pady=12)
        footer.pack(fill="x")
        tk.Button(footer, text="⬅  BACK",
                  bg=BTN_GREY, fg=TEXT_WHITE,
                  font=FONT_BTN, width=20, height=2,
                  bd=0, cursor="hand2", relief="flat",
                  command=self.go_back).pack()
       

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        records = self.model.get_all_counselors()
        for r in records:
            self.tree.insert("", "end", values=(
                r['counselor_id'], r['name'], r['email'],
                r['contact'], r['username'], r['created_at']
            ))

    def go_back(self):
        self.root.destroy()
        self.prev_root.deiconify()
