import customtkinter as ctk


class ReportsPage(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.master = master
        self.pack(fill="both", expand=True)

        # =====================================
        # COLORS
        # =====================================

        self.sidebar_color = "#1E293B"
        self.main_color = "#F5F7FA"
        self.blue = "#2563EB"

        # =====================================
        # SIDEBAR
        # =====================================

        self.sidebar = ctk.CTkFrame(
            self,
            width=240,
            fg_color=self.sidebar_color,
            corner_radius=0
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Logo

        ctk.CTkLabel(
            self.sidebar,
            text="BIOMETRIC\nATTENDANCE",
            font=("Arial",30,"bold"),
            text_color="white"
        ).pack(pady=(40,10))

        ctk.CTkLabel(
            self.sidebar,
            text="Administrator Panel",
            font=("Arial",16),
            text_color="#CBD5E1"
        ).pack(pady=(0,35))

        # Sidebar Buttons

        menus = [
            "🏠 Dashboard",
            "👨‍🎓 Students",
            "📷 Attendance",
            "📄 Reports",
            "⚙ Settings"
        ]

        for menu in menus:

            if menu == "📄 Reports":
                color = self.blue
                hover = "#1D4ED8"
            else:
                color = "#334155"
                hover = "#475569"

            ctk.CTkButton(
                self.sidebar,
                text=menu,
                height=45,
                fg_color=color,
                hover_color=hover,
                corner_radius=8
            ).pack(fill="x", padx=18, pady=8)

        # Logout

        ctk.CTkButton(
            self.sidebar,
            text="Logout",
            fg_color="red",
            hover_color="#8B0000",
            height=45
        ).pack(side="bottom", fill="x", padx=18, pady=20)

        # =====================================
        # SCROLLABLE MAIN AREA
        # =====================================

        self.main = ctk.CTkScrollableFrame(
            self,
            fg_color=self.main_color,
            corner_radius=0
        )

        self.main.pack(
            side="right",
            fill="both",
            expand=True
        )
        self.main.grid_columnconfigure(0, weight=1)

        # =====================================
        # HEADER
        # =====================================

        header = ctk.CTkFrame(
            self.main,
            fg_color="transparent",
            height=90
        )

        header.pack(fill="x", padx=30, pady=25)

        left_header = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )

        left_header.pack(side="left")

        ctk.CTkLabel(
            left_header,
            text="Generate Reports",
            font=("Arial",34,"bold"),
            text_color="#1E293B"
        ).pack(anchor="w")

        ctk.CTkLabel(
            left_header,
            text="Create & Export Attendance Reports",
            font=("Arial",18),
            text_color="#64748B"
        ).pack(anchor="w")

        # =====================================
        # CONTENT AREA
        # =====================================

        content = ctk.CTkFrame(
            self.main,
            fg_color="transparent"
        )

        content.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0,25)
        )

        # Left Panel

        self.left = ctk.CTkFrame(
            content,
            width=320,
            corner_radius=15
        )

        self.left.pack(
            side="left",
            fill="y",
            padx=(0,20)
        )

        self.left.pack_propagate(False)

        # Right Panel

        self.right = ctk.CTkFrame(
            content,
            corner_radius=15
        )

        self.right.pack(
            side="right",
            fill="both",
            expand=True
        )

        # Build Page

        self.create_filters()
        self.create_preview()
            # =====================================
    # REPORT FILTERS
    # =====================================

    def create_filters(self):

        ctk.CTkLabel(
            self.left,
            text="Report Filters",
            font=("Arial", 24, "bold")
        ).pack(pady=(20, 15))

        # -----------------------------
        # Student Name
        # -----------------------------

        ctk.CTkLabel(
            self.left,
            text="Student Name",
            font=("Arial", 15, "bold")
        ).pack(anchor="w", padx=20)

        self.student = ctk.CTkEntry(
            self.left,
            width=270,
            height=40,
            placeholder_text="Enter student name"
        )
        self.student.pack(pady=(5, 15))

        # -----------------------------
        # Roll Number
        # -----------------------------

        ctk.CTkLabel(
            self.left,
            text="Roll Number",
            font=("Arial", 15, "bold")
        ).pack(anchor="w", padx=20)

        self.roll = ctk.CTkEntry(
            self.left,
            width=270,
            height=40,
            placeholder_text="Enter roll number"
        )
        self.roll.pack(pady=(5, 15))

        # -----------------------------
        # Department
        # -----------------------------

        ctk.CTkLabel(
            self.left,
            text="Department",
            font=("Arial", 15, "bold")
        ).pack(anchor="w", padx=20)

        self.department = ctk.CTkComboBox(
            self.left,
            width=270,
            values=[
                "All Departments",
                "Computer Science",
                "Information Technology",
                "Electronics",
                "Mechanical",
                "Civil"
            ]
        )
        self.department.set("All Departments")
        self.department.pack(pady=(5, 15))

        # -----------------------------
        # Year
        # -----------------------------

        ctk.CTkLabel(
            self.left,
            text="Year",
            font=("Arial", 15, "bold")
        ).pack(anchor="w", padx=20)

        self.year = ctk.CTkComboBox(
            self.left,
            width=270,
            values=[
                "All Years",
                "1st Year",
                "2nd Year",
                "3rd Year",
                "4th Year"
            ]
        )
        self.year.set("All Years")
        self.year.pack(pady=(5, 15))

        # -----------------------------
        # Date
        # -----------------------------

        ctk.CTkLabel(
            self.left,
            text="Date",
            font=("Arial", 15, "bold")
        ).pack(anchor="w", padx=20)

        self.date = ctk.CTkEntry(
            self.left,
            width=270,
            height=40,
            placeholder_text="DD-MM-YYYY"
        )
        self.date.pack(pady=(5, 15))

        # -----------------------------
        # Status
        # -----------------------------

        ctk.CTkLabel(
            self.left,
            text="Attendance Status",
            font=("Arial", 15, "bold")
        ).pack(anchor="w", padx=20)

        self.status = ctk.CTkComboBox(
            self.left,
            width=270,
            values=[
                "All",
                "Present",
                "Absent",
                "Late"
            ]
        )
        self.status.set("All")
        self.status.pack(pady=(5, 25))

        # -----------------------------
        # Buttons
        # -----------------------------

        ctk.CTkButton(
            self.left,
            text="Generate Report",
            width=270,
            height=45,
            fg_color="#2563EB",
            hover_color="#1D4ED8"
        ).pack(pady=8)

        ctk.CTkButton(
            self.left,
            text="Clear Filters",
            width=270,
            height=45,
            fg_color="#DC2626",
            hover_color="#B91C1C"
        ).pack(pady=8)
            # =====================================
    # REPORT PREVIEW
    # =====================================

    def create_preview(self):

        # Title

        ctk.CTkLabel(
            self.right,
            text="Report Preview",
            font=("Arial",24,"bold")
        ).pack(anchor="w", padx=25, pady=(20,15))

        # =====================================
        # Statistics Cards
        # =====================================

        cards = ctk.CTkFrame(
            self.right,
            fg_color="transparent"
        )
        cards.pack(fill="x", padx=20)

        stats = [
            ("Total Students", "120", "#2563EB"),
            ("Present", "110", "#16A34A"),
            ("Absent", "10", "#DC2626"),
            ("Late", "5", "#F59E0B")
        ]

        for title, value, color in stats:

            card = ctk.CTkFrame(
                cards,
                width=165,
                height=95,
                corner_radius=12
            )
            card.pack(side="left", padx=10)
            card.pack_propagate(False)

            ctk.CTkFrame(
                card,
                height=6,
                fg_color=color
            ).pack(fill="x")

            ctk.CTkLabel(
                card,
                text=title,
                font=("Arial",15)
            ).pack(pady=(12,2))

            ctk.CTkLabel(
                card,
                text=value,
                font=("Arial",28,"bold")
            ).pack()

        # =====================================
        # Attendance Percentage
        # =====================================

        attendance_card = ctk.CTkFrame(
            self.right,
            corner_radius=12
        )
        attendance_card.pack(fill="x", padx=25, pady=20)

        ctk.CTkLabel(
            attendance_card,
            text="Attendance Percentage",
            font=("Arial",18,"bold")
        ).pack(anchor="w", padx=20, pady=(15,5))

        progress = ctk.CTkProgressBar(
            attendance_card,
            width=550,
            height=18
        )

        progress.set(0.92)
        progress.pack(anchor="w", padx=20)

        ctk.CTkLabel(
            attendance_card,
            text="92%",
            font=("Arial",16,"bold"),
            text_color="#16A34A"
        ).pack(anchor="w", padx=20, pady=(8,15))

        # =====================================
        # Report Status
        # =====================================

        status = ctk.CTkFrame(
            self.right,
            corner_radius=12
        )
        status.pack(fill="x", padx=25)

        ctk.CTkLabel(
            status,
            text="Last Generated : Today 09:15 AM",
            font=("Arial",15)
        ).pack(anchor="w", padx=20, pady=(15,5))

        ctk.CTkLabel(
            status,
            text="✓ Report Ready To Export",
            font=("Arial",16,"bold"),
            text_color="#16A34A"
        ).pack(anchor="w", padx=20, pady=(0,15))

        # =====================================
        # Preview Box
        # =====================================

        preview = ctk.CTkFrame(
            self.right,
            height=180,
            corner_radius=12
        )

        preview.pack(fill="x", padx=25, pady=20)
        preview.pack_propagate(False)

        ctk.CTkLabel(
            preview,
            text="Report Preview Area",
            font=("Arial",22,"bold")
        ).pack(pady=(30,10))

        ctk.CTkLabel(
            preview,
            text="Generated attendance reports will appear here.\n\n"
                 "You can later display tables, charts,\n"
                 "or attendance summaries.",
            justify="center",
            font=("Arial",15)
        ).pack()

        # =====================================
        # Export Buttons
        # =====================================

        export = ctk.CTkFrame(
            self.right,
            fg_color="transparent"
        )

        export.pack(fill="x", pady=(20,35))

        ctk.CTkButton(
            export,
            text="📊 Export Excel",
            width=180,
            height=45
        ).pack(side="left", padx=20)

        ctk.CTkButton(
            export,
            text="📄 Export PDF",
            width=180,
            height=45
        ).pack(side="left", padx=20)

        ctk.CTkButton(
            export,
            text="🖨 Print Report",
            width=180,
            height=45,
            fg_color="#16A34A",
            hover_color="#15803D"
        ).pack(side="left", padx=20)