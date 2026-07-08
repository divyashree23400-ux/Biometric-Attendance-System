import customtkinter as ctk
from tkinter import messagebox
from database.firebase import students_db


class StudentsPage(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.master = master
        self.pack(fill="both", expand=True)

        # ==========================
        # Colors
        # ==========================

        self.sidebar_color = "#1E293B"
        self.main_color = "#F8FAFC"
        self.blue = "#2563EB"

        # Selected student
        self.selected_roll = None

        # Build UI
        self.create_sidebar()
        self.create_main()

    # =====================================
    # Sidebar
    # =====================================

    def create_sidebar(self):

        self.sidebar = ctk.CTkFrame(
            self,
            width=240,
            fg_color=self.sidebar_color,
            corner_radius=0
        )

        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        ctk.CTkLabel(
            self.sidebar,
            text="BIOMETRIC\nATTENDANCE",
            font=("Arial", 28, "bold"),
            text_color="white"
        ).pack(pady=(40, 10))

        ctk.CTkLabel(
            self.sidebar,
            text="Administrator Panel",
            font=("Arial", 16),
            text_color="#CBD5E1"
        ).pack(pady=(0, 35))

        menus = [
            "🏠 Dashboard",
            "👨‍🎓 Students",
            "📷 Attendance",
            "📄 Reports",
            "⚙ Settings"
        ]

        for menu in menus:

            color = self.blue if menu == "👨‍🎓 Students" else "#334155"

            ctk.CTkButton(
                self.sidebar,
                text=menu,
                height=45,
                fg_color=color
            ).pack(fill="x", padx=20, pady=7)

        ctk.CTkButton(
            self.sidebar,
            text="Logout",
            fg_color="red",
            height=45
        ).pack(side="bottom", fill="x", padx=20, pady=20)

    # =====================================
    # Main Window
    # =====================================

    def create_main(self):

        self.main = ctk.CTkFrame(
            self,
            fg_color=self.main_color,
            corner_radius=0
        )

        self.main.pack(
            side="right",
            fill="both",
            expand=True
        )

        header = ctk.CTkFrame(
            self.main,
            fg_color="transparent"
        )

        header.pack(fill="x", padx=25, pady=20)

        left = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )

        left.pack(side="left")

        ctk.CTkLabel(
            left,
            text="Student Management",
            font=("Arial", 34, "bold")
        ).pack(anchor="w")

        ctk.CTkLabel(
            left,
            text="Manage Student Records",
            font=("Arial", 18)
        ).pack(anchor="w")

        content = ctk.CTkFrame(
            self.main,
            fg_color="transparent"
        )

        content.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

        self.left = ctk.CTkFrame(
            content,
            width=350
        )

        self.left.pack(
            side="left",
            fill="y",
            padx=(0, 20)
        )

        self.left.pack_propagate(False)

        self.right = ctk.CTkFrame(content)

        self.right.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.create_form()
        self.create_table()
        self.load_students()
            # =====================================
    # STUDENT FORM
    # =====================================

    def create_form(self):

        ctk.CTkLabel(
            self.left,
            text="Student Details",
            font=("Arial", 24, "bold")
        ).pack(pady=20)

        # ---------- Student Name ----------

        ctk.CTkLabel(
            self.left,
            text="Student Name",
            font=("Arial", 15, "bold")
        ).pack(anchor="w", padx=20)

        self.name = ctk.CTkEntry(
            self.left,
            width=300,
            height=40,
            placeholder_text="Enter Student Name"
        )
        self.name.pack(pady=(5, 15))

        # ---------- Roll Number ----------

        ctk.CTkLabel(
            self.left,
            text="Roll Number",
            font=("Arial", 15, "bold")
        ).pack(anchor="w", padx=20)

        self.roll = ctk.CTkEntry(
            self.left,
            width=300,
            height=40,
            placeholder_text="Enter Roll Number"
        )
        self.roll.pack(pady=(5, 15))

        # ---------- Department ----------

        ctk.CTkLabel(
            self.left,
            text="Department",
            font=("Arial", 15, "bold")
        ).pack(anchor="w", padx=20)

        self.department = ctk.CTkComboBox(
            self.left,
            width=300,
            values=[
                "Computer Science",
                "Information Technology",
                "Electronics",
                "Mechanical",
                "Civil"
            ]
        )
        self.department.pack(pady=(5, 15))
        self.department.set("Computer Science")

        # ---------- Year ----------

        ctk.CTkLabel(
            self.left,
            text="Year",
            font=("Arial", 15, "bold")
        ).pack(anchor="w", padx=20)

        self.year = ctk.CTkComboBox(
            self.left,
            width=300,
            values=[
                "1st Year",
                "2nd Year",
                "3rd Year",
                "4th Year"
            ]
        )
        self.year.pack(pady=(5, 15))
        self.year.set("1st Year")

        # ---------- Email ----------

        ctk.CTkLabel(
            self.left,
            text="Email",
            font=("Arial", 15, "bold")
        ).pack(anchor="w", padx=20)

        self.email = ctk.CTkEntry(
            self.left,
            width=300,
            height=40,
            placeholder_text="Enter Email Address"
        )
        self.email.pack(pady=(5, 15))

        # ---------- Phone ----------

        ctk.CTkLabel(
            self.left,
            text="Phone Number",
            font=("Arial", 15, "bold")
        ).pack(anchor="w", padx=20)

        self.phone = ctk.CTkEntry(
            self.left,
            width=300,
            height=40,
            placeholder_text="Enter Phone Number"
        )
        self.phone.pack(pady=(5, 25))

        # ---------- Buttons ----------
        self.add_btn = ctk.CTkButton(
            self.left,
            text="➕ Add Student",
            width=300,
            height=45,
            command=self.add_student
        )

        self.add_btn.pack(pady=5)

        

        self.update_btn = ctk.CTkButton(
            self.left,
            text="✏ Update Student",
            width=300,
            height=45,
            fg_color="#16A34A",
            hover_color="#15803D",
            command=self.update_student
        )
        self.update_btn.pack(pady=5)

        self.delete_btn = ctk.CTkButton(
            self.left,
            text="🗑 Delete Student",
            width=300,
            height=45,
            fg_color="#DC2626",
            hover_color="#B91C1C"
        )
        self.delete_btn.pack(pady=5)

        
       # =====================================
    # STUDENT TABLE
    # =====================================

    def create_table(self):

        ctk.CTkLabel(
            self.right,
            text="Student Records",
            font=("Arial", 24, "bold")
        ).pack(anchor="w", padx=20, pady=(20, 10))

        # ---------------- Search ----------------

        search_frame = ctk.CTkFrame(
            self.right,
            fg_color="transparent"
        )

        search_frame.pack(fill="x", padx=20)

        self.search = ctk.CTkEntry(
            search_frame,
            width=400,
            placeholder_text="Search by Roll Number..."
        )

        self.search.pack(side="left", padx=(0,10))

        self.search_btn = ctk.CTkButton(
            search_frame,
            text="Search",
            width=120
        )

        self.search_btn.pack(side="left")

        # ---------------- Header ----------------

        header = ctk.CTkFrame(
            self.right,
            height=40
        )

        header.pack(fill="x", padx=20, pady=(20,5))

        headings = [
            "Roll No",
            "Name",
            "Department",
            "Year"
        ]

        for text in headings:

            ctk.CTkLabel(
                header,
                text=text,
                width=170,
                font=("Arial",15,"bold")
            ).pack(side="left", padx=5, pady=10)

        # ---------------- Scrollable Table ----------------

        self.table = ctk.CTkScrollableFrame(
            self.right,
            height=500
        )

        self.table.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0,20)
        )
            # =====================================
    # LOAD STUDENTS FROM FIREBASE
    # =====================================

    def load_students(self):

        # Clear previous rows
        for widget in self.table.winfo_children():
            widget.destroy()

        data = students_db.get()

        if not data:
            return

        for roll, student in data.items():

            row = ctk.CTkFrame(
                self.table,
                cursor="hand2"
            )

            row.pack(fill="x", pady=3)

            row.bind(
                "<Button-1>",
                lambda e, r=roll: self.select_student(r)
            )

            label = ctk.CTkLabel(
                row,
                text=roll,
                width=170  
            )

            label.pack(side="left", padx=5, pady=8)

            label.bind(
                "<Button-1>",
                lambda e, r=roll: self.select_student(r)
            )
            label = ctk.CTkLabel(
                row,
                text=student.get("name",""),
                width=170
            )

            label.pack(side="left", padx=5)

            label.bind(
                "<Button-1>",
                lambda e, r=roll: self.select_student(r)
            )

            label = ctk.CTkLabel(
                row,
                text=student.get("department", ""),
                width=170
            )

            label.pack(side="left", padx=5)

            label.bind(
                "<Button-1>",
                lambda e, r=roll: self.select_student(r)
            )

            label = ctk.CTkLabel(
                row,
                text=student.get("year", ""),
                width=170
            )

            label.pack(side="left", padx=5)

            label.bind(
                "<Button-1>",
                lambda e, r=roll: self.select_student(r)
            )

    # =====================================
    # CLEAR FORM
    # =====================================

    def clear_fields(self):

        self.name.delete(0, "end")
        self.roll.delete(0, "end")
        self.email.delete(0, "end")
        self.phone.delete(0, "end")

        self.department.set("Computer Science")
        self.year.set("1st Year")

        self.selected_roll = None
            # =====================================
    # ADD STUDENT
    # =====================================

    def add_student(self):

        name = self.name.get().strip()
        roll = self.roll.get().strip()
        department = self.department.get()
        year = self.year.get()
        email = self.email.get().strip()
        phone = self.phone.get().strip()

        if name == "" or roll == "":
            messagebox.showerror(
                "Error",
                "Student Name and Roll Number are required."
            )
            return

        students_db.child(roll).set({

            "name": name,
            "department": department,
            "year": year,
            "email": email,
            "phone": phone

        })

        messagebox.showinfo(
            "Success",
            "Student Added Successfully!"
        )

        self.clear_fields()
        self.load_students()
            # =====================================
    # UPDATE STUDENT
    # =====================================

    def update_student(self):

        if self.selected_roll is None:

            messagebox.showwarning(
                "Warning",
                "Select a student first."
            )
            return

        name = self.name.get().strip()
        roll = self.roll.get().strip()
        department = self.department.get()
        year = self.year.get()
        email = self.email.get().strip()
        phone = self.phone.get().strip()

        students_db.child(self.selected_roll).update({

            "name": name,
            "department": department,
            "year": year,
            "email": email,
            "phone": phone

        })

        messagebox.showinfo(
            "Success",
            "Student Updated Successfully!"
        )

        self.clear_fields()
        self.load_students()
            # =====================================
    # DELETE STUDENT
    # =====================================

    def delete_student(self):

        if self.selected_roll is None:

            messagebox.showwarning(
                "Warning",
                "Select a student first."
            )
            return

        answer = messagebox.askyesno(
            "Delete Student",
            "Are you sure you want to delete this student?"
        )

        if not answer:
            return

        students_db.child(self.selected_roll).delete()

        messagebox.showinfo(
            "Success",
            "Student Deleted Successfully!"
        )

        self.clear_fields()
        self.load_students()
            # =====================================
    # SELECT STUDENT
    # =====================================

    def select_student(self, roll):

        student = students_db.child(roll).get()

        if not student:
            return

        self.selected_roll = roll

        self.name.delete(0, "end")
        self.name.insert(0, student.get("name", ""))

        self.roll.delete(0, "end")
        self.roll.insert(0, roll)

        self.department.set(student.get("department", ""))

        self.year.set(student.get("year", ""))

        self.email.delete(0, "end")
        self.email.insert(0, student.get("email", ""))

        self.phone.delete(0, "end")
        self.phone.insert(0, student.get("phone", ""))

