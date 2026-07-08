import customtkinter as ctk


class AttendancePage(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.master = master
        self.pack(fill="both", expand=True)

        # ----------------------------
        # Colors
        # ----------------------------

        self.sidebar_color = "#1E293B"
        self.main_color = "#F5F7FA"
        self.card_color = "#FFFFFF"
        self.blue = "#2563EB"

        # ----------------------------
        # Sidebar
        # ----------------------------

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
        ).pack(pady=(0,40))

        # Sidebar Buttons

        menu = [

            "🏠 Dashboard",
            "👨‍🎓 Students",
            "📷 Attendance",
            "📄 Reports",
            "⚙ Settings"

        ]

        for item in menu:

            if item == "📷 Attendance":
                color = self.blue
                hover = "#1D4ED8"
            else:
                color = "#334155"
                hover = "#475569"

            ctk.CTkButton(
                self.sidebar,
                text=item,
                height=45,
                fg_color=color,
                hover_color=hover,
                corner_radius=8
            ).pack(fill="x", padx=18, pady=10)

        # Logout Button

        ctk.CTkButton(
            self.sidebar,
            text="Logout",
            fg_color="red",
            hover_color="darkred",
            height=45
        ).pack(side="bottom", fill="x", padx=18, pady=20)

        # ----------------------------
        # Main Area
        # ----------------------------

        self.main = ctk.CTkFrame(
            self,
            fg_color=self.main_color,
            corner_radius=0
        )
        self.main.pack(side="right", fill="both", expand=True)

        # ----------------------------
        # Header
        # ----------------------------

        header = ctk.CTkFrame(
            self.main,
            fg_color="transparent",
            height=90
        )
        header.pack(fill="x", padx=30, pady=25)

        ctk.CTkLabel(
            header,
            text="Attendance Management",
            font=("Arial",34,"bold"),
            text_color="#1E293B"
        ).pack(anchor="w")

        ctk.CTkLabel(
            header,
            text="Manage student attendance records",
            font=("Arial",18),
            text_color="#64748B"
        ).pack(anchor="w")

        # ----------------------------
        # Main Container
        # ----------------------------

        container = ctk.CTkFrame(
            self.main,
            fg_color="transparent"
        )
        container.pack(fill="both", expand=True, padx=25, pady=10)

        # Left Panel

        self.left = ctk.CTkFrame(
            container,
            width=360,
            corner_radius=15
        )
        self.left.pack(side="left", fill="y", padx=(0,20))
        self.left.pack_propagate(False)

        # Right Panel

        self.right = ctk.CTkFrame(
            container,
            corner_radius=15
        )
        self.right.pack(side="right", fill="both", expand=True)

        # Build UI

        self.create_camera_section()
        self.create_attendance_table()
            # =========================================
    # CAMERA SECTION
    # =========================================

    def create_camera_section(self):

        ctk.CTkLabel(
            self.left,
            text="Camera Preview",
            font=("Arial", 24, "bold")
        ).pack(pady=20)

        # Camera Preview Box

        self.camera_frame = ctk.CTkFrame(
            self.left,
            width=300,
            height=250,
            corner_radius=15,
            fg_color="#2E2E2E"
        )
        self.camera_frame.pack(pady=15)
        self.camera_frame.pack_propagate(False)

        ctk.CTkLabel(
            self.camera_frame,
            text="📷\n\nCamera Preview\n\n(Preview will appear here)",
            font=("Arial", 18),
            justify="center"
        ).place(relx=0.5, rely=0.5, anchor="center")

        # =============================
        # Camera Controls
        # =============================

        ctk.CTkButton(
            self.left,
            text="▶ Start Camera",
            width=300,
            height=45,
            fg_color=self.blue,
            hover_color="#1D4ED8"
        ).pack(pady=(20,10))

        ctk.CTkButton(
            self.left,
            text="⏹ Stop Camera",
            width=300,
            height=45,
            fg_color="#DC2626",
            hover_color="#B91C1C"
        ).pack(pady=10)

        ctk.CTkButton(
            self.left,
            text="📸 Capture Face",
            width=300,
            height=45
        ).pack(pady=10)

        ctk.CTkButton(
            self.left,
            text="✅ Mark Attendance",
            width=300,
            height=45,
            fg_color="#16A34A",
            hover_color="#15803D"
        ).pack(pady=10)

        # Today's Summary

        summary = ctk.CTkFrame(
            self.left,
            corner_radius=12
        )
        summary.pack(fill="x", padx=15, pady=20)

        ctk.CTkLabel(
            summary,
            text="Today's Summary",
            font=("Arial",18,"bold")
        ).pack(pady=(10,5))

        ctk.CTkLabel(
            summary,
            text="Present : 110",
            font=("Arial",16)
        ).pack()

        ctk.CTkLabel(
            summary,
            text="Absent : 10",
            font=("Arial",16)
        ).pack()

        ctk.CTkLabel(
            summary,
            text="Late : 5",
            font=("Arial",16)
        ).pack(pady=(0,10))
            # =========================================
    # ATTENDANCE TABLE
    # =========================================

    def create_attendance_table(self):

        ctk.CTkLabel(
            self.right,
            text="Attendance Records",
            font=("Arial",24,"bold")
        ).pack(pady=(20,10))

        # ----------------------------
        # Search Bar
        # ----------------------------

        search_frame = ctk.CTkFrame(
            self.right,
            fg_color="transparent"
        )
        search_frame.pack(fill="x", padx=20, pady=(0,15))

        self.search = ctk.CTkEntry(
            search_frame,
            width=350,
            placeholder_text="Search by Name or Roll Number"
        )
        self.search.pack(side="left")

        ctk.CTkButton(
            search_frame,
            text="Search",
            width=120
        ).pack(side="left", padx=10)

        # ----------------------------
        # Table Header
        # ----------------------------

        header = ctk.CTkFrame(
            self.right,
            corner_radius=10
        )
        header.pack(fill="x", padx=20)

        headings = [
            "Roll No",
            "Student Name",
            "Date",
            "Time",
            "Status"
        ]

        for heading in headings:

            ctk.CTkLabel(
                header,
                text=heading,
                width=135,
                font=("Arial",15,"bold")
            ).pack(side="left", pady=10)

        # ----------------------------
        # Scrollable Records
        # ----------------------------

        body = ctk.CTkScrollableFrame(
            self.right,
            height=450
        )
        body.pack(fill="both", expand=True, padx=20, pady=10)

        attendance = [

            ("101","Krishna","15-05-2026","09:00 AM","Present"),
            ("102","Rahul Sharma","15-05-2026","09:03 AM","Present"),
            ("103","Anjali Patel","15-05-2026","09:05 AM","Late"),
            ("104","Amit Kumar","15-05-2026","09:01 AM","Present"),
            ("105","Priya Verma","15-05-2026","09:08 AM","Absent"),
            ("106","Arjun Singh","15-05-2026","09:06 AM","Present"),
            ("107","Sneha Reddy","15-05-2026","09:02 AM","Present"),
            ("108","Vikram Joshi","15-05-2026","09:09 AM","Late"),
            ("109","Neha Gupta","15-05-2026","09:04 AM","Present"),
            ("110","Rohan Mehta","15-05-2026","09:07 AM","Present")

        ]

        for roll, name, date, time, status in attendance:

            row = ctk.CTkFrame(body)
            row.pack(fill="x", pady=5)

            ctk.CTkLabel(
                row,
                text=roll,
                width=135
            ).pack(side="left")

            ctk.CTkLabel(
                row,
                text=name,
                width=135
            ).pack(side="left")

            ctk.CTkLabel(
                row,
                text=date,
                width=135
            ).pack(side="left")

            ctk.CTkLabel(
                row,
                text=time,
                width=135
            ).pack(side="left")

            if status == "Present":
                color = "#16A34A"

            elif status == "Late":
                color = "#F59E0B"

            else:
                color = "#DC2626"

            ctk.CTkLabel(
                row,
                text=status,
                width=135,
                text_color=color,
                font=("Arial",14,"bold")
            ).pack(side="left")