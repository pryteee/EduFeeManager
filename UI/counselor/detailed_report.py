import tkinter as tk
from tkinter import ttk, messagebox
from models.fee_model import FeeModel
from UI.styles import (
    BG_DARK, BG_CARD, ACCENT, BTN_BLUE, BTN_GREY,
    TEXT_WHITE, TEXT_MUTED, TEXT_SUCCESS, TEXT_WARN, TEXT_DANGER,
    FONT_TITLE, FONT_SUBTITLE, FONT_BTN, FONT_LABEL
)


class DetailedReport:
    def __init__(self, root, prev_root):
        self.root      = root
        self.prev_root = prev_root
        self.model     = FeeModel()
        self.root.title("Counselor — Detailed Fee Report")
        self.root.state("zoomed")
        self.root.configure(bg=BG_DARK)
        self.root.protocol("WM_DELETE_WINDOW", self.go_back)
        self.build_ui()

    def build_ui(self):
        header = tk.Frame(self.root, bg=BG_DARK, pady=20)
        header.pack(fill="x", padx=30)

        tk.Label(header,
                 text="DETAILED FEE REPORT",
                 font=FONT_TITLE,
                 bg=BG_DARK, fg=ACCENT).pack()

        tk.Label(header,
                 text="Complete fee status of all students",
                 font=FONT_SUBTITLE,
                 bg=BG_DARK, fg=TEXT_MUTED).pack(pady=(4, 0))

        filter_frame = tk.Frame(self.root, bg=BG_DARK, padx=30)
        filter_frame.pack(fill="x", pady=(0, 10))

        tk.Label(filter_frame, text="Filter by Status:",
                 font=FONT_LABEL, bg=BG_DARK,
                 fg=TEXT_WHITE).pack(side="left", padx=(0, 10))

        self.filter_var = tk.StringVar(value="All")

        filters = ["All", "Pending", "Partial Paid", "Fully Paid"]
        btn_colors = {
            "All":          BTN_BLUE,
            "Pending":      "#e94560",
            "Partial Paid": "#b8860b",
            "Fully Paid":   "#1a6b3c",
        }

        for f in filters:
            tk.Button(filter_frame,
                      text=f,
                      bg=btn_colors[f],
                      fg=TEXT_WHITE,
                      font=FONT_BTN,
                      width=12, height=1,
                      bd=0, cursor="hand2",
                      relief="flat",
                      command=lambda x=f: self.apply_filter(x)
                      ).pack(side="left", padx=4)

        self.summary_frame = tk.Frame(self.root, bg=BG_CARD,
                                      padx=30, pady=12)
        self.summary_frame.pack(fill="x", padx=30, pady=(0, 10))

        self.lbl_total    = tk.Label(self.summary_frame, text="Total: 0",
                                     font=FONT_LABEL, bg=BG_CARD,
                                     fg=TEXT_WHITE)
        self.lbl_total.pack(side="left", padx=(0, 20))

        self.lbl_fp = tk.Label(self.summary_frame, text="Fully Paid: 0",
                               font=FONT_LABEL, bg=BG_CARD,
                               fg=TEXT_SUCCESS)
        self.lbl_fp.pack(side="left", padx=(0, 20))

        self.lbl_pp = tk.Label(self.summary_frame, text="Partial Paid: 0",
                               font=FONT_LABEL, bg=BG_CARD,
                               fg=TEXT_WARN)
        self.lbl_pp.pack(side="left", padx=(0, 20))

        self.lbl_pd = tk.Label(self.summary_frame, text="Pending: 0",
                               font=FONT_LABEL, bg=BG_CARD,
                               fg=TEXT_DANGER)
        self.lbl_pd.pack(side="left", padx=(0, 20))

        self.lbl_collection = tk.Label(self.summary_frame,
                                       text="Collection: ₹0.00",
                                       font=FONT_LABEL, bg=BG_CARD,
                                       fg=TEXT_SUCCESS)
        self.lbl_collection.pack(side="left", padx=(0, 20))

        self.lbl_pending_amt = tk.Label(self.summary_frame,
                                        text="Total Pending: ₹0.00",
                                        font=FONT_LABEL, bg=BG_CARD,
                                        fg=TEXT_DANGER)
        self.lbl_pending_amt.pack(side="left")

        tree_frame = tk.Frame(self.root, bg=BG_DARK, padx=30)
        tree_frame.pack(fill="both", expand=True)

        cols = (
            "ID", "Name", "Course",
            "Year", "Course Fee",
            "Paid", "Pending", "Status"
        )

        self.tree = ttk.Treeview(tree_frame,
                                 columns=cols,
                                 show="headings",
                                 selectmode="browse")

        col_widths = {
            "ID":         60,
            "Name":       180,
            "Course":     130,
            "Year":       70,
            "Course Fee": 110,
            "Paid":       110,
            "Pending":    110,
            "Status":     110,
        }
        for col in cols:
            self.tree.heading(col, text=col,
                              command=lambda c=col: self.sort_by(c))
            self.tree.column(col,
                             width=col_widths[col],
                             anchor="center",
                             minwidth=50)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background=BG_CARD,
                        fieldbackground=BG_CARD,
                        foreground=TEXT_WHITE,
                        rowheight=32,
                        font=("Helvetica", 11))
        style.configure("Treeview.Heading",
                        background="#0f3460",
                        foreground=TEXT_WHITE,
                        font=("Helvetica", 11, "bold"))
        style.map("Treeview",
                  background=[("selected", ACCENT)])

        self.tree.tag_configure("fully_paid",
                                foreground="#00c851")
        self.tree.tag_configure("partial_paid",
                                foreground="#ffbb33")
        self.tree.tag_configure("pending",
                                foreground="#e94560")
        self.tree.tag_configure("no_fee",
                                foreground="#666680")

        vsb = ttk.Scrollbar(tree_frame, orient="vertical",
                            command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal",
                            command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set,
                            xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)

        footer = tk.Frame(self.root, bg=BG_DARK, pady=12)
        footer.pack(fill="x", padx=30)

        btn_cfg = dict(font=FONT_BTN, width=18, height=2,
                       bd=0, cursor="hand2", relief="flat")

        tk.Button(footer, text="🔄  REFRESH",
                  bg=BTN_BLUE, fg=TEXT_WHITE,
                  command=self.load_data,
                  **btn_cfg).pack(side="left", padx=(0, 10))

        tk.Button(footer, text="⬅  BACK",
                  bg=BTN_GREY, fg=TEXT_WHITE,
                  command=self.go_back,
                  **btn_cfg).pack(side="left")

        search_frame = tk.Frame(footer, bg=BG_DARK)
        search_frame.pack(side="right")

        tk.Label(search_frame, text="🔍 Search:",
                 font=FONT_LABEL, bg=BG_DARK,
                 fg=TEXT_WHITE).pack(side="left", padx=(0, 6))

        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *a: self.apply_search())

        tk.Entry(search_frame,
                 textvariable=self.search_var,
                 width=22,
                 font=("Helvetica", 11),
                 bg="#0f3460", fg=TEXT_WHITE,
                 insertbackground=TEXT_WHITE,
                 relief="flat", bd=6
                 ).pack(side="left")

        self.all_data   = []
        self.sort_col   = None
        self.sort_asc   = True
        self.load_data()

    def load_data(self):
        """Fetch all records and display them."""
        self.all_data = self.model.get_all_students_fee_report()
        self.filter_var.set("All")
        self.search_var.set("")
        self.populate_tree(self.all_data)
        self.update_summary(self.all_data)

    def populate_tree(self, data):
        """Clear and fill treeview with given data."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        for r in data:
            status = r['status']

            
            if status == "Fully Paid":
                tag = "fully_paid"
            elif status == "Partial Paid":
                tag = "partial_paid"
            elif float(r['course_fee']) == 0:
                tag = "no_fee"
            else:
                tag = "pending"

            self.tree.insert("", "end", tags=(tag,), values=(
                r['student_id'],
                r['name'],
                r['course'],
                r['academic_year'],
                f"₹{float(r['course_fee']):.2f}",
                f"₹{float(r['paid_amount']):.2f}",
                f"₹{float(r['pending_amount']):.2f}",
                status
            ))

    
    def update_summary(self, data):
        """Update the summary strip above the table."""
        total    = len(data)
        fp       = sum(1 for r in data if r['status'] == 'Fully Paid')
        pp       = sum(1 for r in data if r['status'] == 'Partial Paid')
        pd       = sum(1 for r in data if r['status'] == 'Pending')
        collect  = sum(float(r['paid_amount'])    for r in data)
        pend_amt = sum(float(r['pending_amount']) for r in data)

        self.lbl_total.config(
            text=f"Total: {total}")
        self.lbl_fp.config(
            text=f"Fully Paid: {fp}")
        self.lbl_pp.config(
            text=f"Partial Paid: {pp}")
        self.lbl_pd.config(
            text=f"Pending: {pd}")
        self.lbl_collection.config(
            text=f"Collection: ₹{collect:.2f}")
        self.lbl_pending_amt.config(
            text=f"Total Pending: ₹{pend_amt:.2f}")

    def apply_filter(self, status):
        """Filter rows by payment status."""
        self.filter_var.set(status)
        self.search_var.set("")

        if status == "All":
            filtered = self.all_data
        else:
            filtered = [
                r for r in self.all_data
                if r['status'] == status
            ]

        self.populate_tree(filtered)
        self.update_summary(filtered)

    def apply_search(self):
        """Search by student name, ID, or course."""
        query = self.search_var.get().strip().lower()

        if not query:
            self.populate_tree(self.all_data)
            self.update_summary(self.all_data)
            return

        filtered = [
            r for r in self.all_data
            if query in str(r['student_id']).lower()
            or query in r['name'].lower()
            or query in r['course'].lower()
            or query in r['status'].lower()
        ]

        self.populate_tree(filtered)
        self.update_summary(filtered)

    def sort_by(self, col):
        """Sort treeview by clicking column header."""
        col_map = {
            "ID":         "student_id",
            "Name":       "name",
            "Course":     "course",
            "Year":       "academic_year",
            "Course Fee": "course_fee",
            "Paid":       "paid_amount",
            "Pending":    "pending_amount",
            "Status":     "status",
        }
        key = col_map.get(col, "student_id")

        if self.sort_col == col:
            self.sort_asc = not self.sort_asc
        else:
            self.sort_col = col
            self.sort_asc = True

        try:
            sorted_data = sorted(
                self.all_data,
                key=lambda r: float(r[key])
                    if key in ("course_fee", "paid_amount",
                               "pending_amount", "academic_year",
                               "student_id")
                    else str(r[key]).lower(),
                reverse=not self.sort_asc
            )
        except Exception:
            sorted_data = self.all_data

        self.populate_tree(sorted_data)

    def go_back(self):
        self.root.destroy()
        self.prev_root.deiconify()
