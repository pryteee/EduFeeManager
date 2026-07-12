# EduFeeManager

A desktop-based fee management application developed during our internship to help institutions manage student fee records in a simple and organized way.

The application is built using **Python (Tkinter)** for the user interface and **MySQL** for database management. It works completely offline and does not require an internet connection.

---

## About the Project

Managing student fee records manually through registers or spreadsheets can be difficult, time-consuming, and prone to errors.

This project provides a digital solution where administrators, counselors, and students have separate portals based on their roles.

The system helps manage:

- Student information
- Course details
- Fee structure
- Paid and pending amounts
- Payment status
- Fee reports

The main goal of this project is to make fee management easier, faster, and more organized.

---

##  Features

###  Admin
- Register and login securely
- Add new counselors to the system
- Edit or delete existing counselor accounts
- View individual counselor details
- View all counselors in a single table
- Delete student accounts when required
- Forgot password and change password options

###  Counselor
- Register and login securely
- Add new students with course details
- Update student information
- Assign and edit fee structure for each student
- Set course fee, paid amount — pending is auto-calculated
- Fee status is automatically determined:
  - **Pending** — no payment made
  - **Partial Paid** — some payment made
  - **Fully Paid** — complete payment received
- View fee summary report with totals
- View detailed report showing every student's fee status
  with filters by payment status and live search
- Forgot password and change password options

###  Student
- Self-register with personal and course details
- Login using Student ID, username and password
- View personal enrollment and course details
- View current payment status with color indicators
  -  Fully Paid
  -  Partial Paid
  -  Pending
- Forgot password and change password options

---

## Installation

### Requirements
- Python 3.x
- MySQL Server
- Pillow library
- mysql-connector-python library


---

##  How to Use

### Step 1 — Clone the repository

```bash
git clone https://github.com/pryteee/EduFeeManager
cd EduFeeManager
```

---

### Step 2 — Install dependencies

```bash
pip install -r requirements.txt
```

---

### Step 3 — Setup the database

The complete database schema is available in `schema.sql`.

Run it directly from terminal:

```bash
mysql -u root -p < schema.sql
```

Or open MySQL command line and run:

```bash
source schema.sql
```

---

### Step 4 — Configure database connection

Open `database/db_connection.py` and update your
MySQL credentials:

```python
self.host     = "localhost"
self.user     = "root"           # your MySQL username
self.password = "your_password"  # your MySQL password
self.database = "fee_structure_management"
```

---


### Step 5 — Run the application

```bash
python main.py
```

---

### Step 7 — Using the application

**First time setup — follow this order:**

```
1. Open app → click ADMIN → Register → note your Admin ID
2. Login as Admin → Add a Counselor from the dashboard
3. Open app → click COUNSELOR → Login
4. Add students and assign their fee structure
5. Students can now Register and Login to view their fees
```

---

**Admin**
- Register once and note your Admin ID
- Login to manage counselors — add, edit, delete or view
- Delete student accounts if needed
- Use forgot password if you forget your password

**Counselor**
- Login with username and password given during registration
- Add students with their course details
- Go to **Edit Fee Structure** → enter Student ID →
  set course fee and paid amount → status is auto-calculated
- Use **Reports** for a quick summary
- Use **Detailed Report** to see all students with
  filters by payment status and live name search

**Student**
- Register and save your **Student ID** shown after registration
- Login with Student ID + username + password
- View your fee details and payment status from the dashboard
- Contact your counselor if fee details are not updated yet

---

##  Important Notes

- Students must save their **Student ID** shown after
  registration — it cannot be recovered without it
- Fee details for students are managed only by the
  **Counselor** — students cannot edit their own fees
- Passwords can be reset using the
  **Forgot Password** option on the login page

---

