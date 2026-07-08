import customtkinter as ctk
from datetime import datetime


class Dashboard(ctk.CTkFrame):

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
            font=("Arial", 30, "bold"),
            text_color="white"
        ).pack(pady=(40, 10))

        ctk.CTkLabel(
            self.sidebar,
            text="Administrator Panel",
            font=("Arial", 16),
            text_color="#CBD5E1"
        ).pack(pady=(0, 40))

        # Sidebar Buttons

        menu = [
            "🏠 Dashboard",
            "👨‍🎓 Students",
            "📷 Attendance",
            "📄 Reports",
            "⚙ Settings"
        ]

        for item in menu:

            ctk.CTkButton(
                self.sidebar,
                text=item,
                height=45,
                fg_color=self.blue,
                hover_color="#1D4ED8",
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

        # Build UI

        self.create_header()

    # =====================================
    # HEADER
    # =====================================

    def create_header(self):

        header = ctk.CTkFrame(
            self.main,
            fg_color="transparent",
            height=90
        )
        header.pack(fill="x", padx=30, pady=25)

        left = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )
        left.pack(side="left")

        ctk.CTkLabel(
            left,
            text="Dashboard",
            font=("Arial", 34, "bold"),
            text_color="#1E293B"
        ).pack(anchor="w")

        ctk.CTkLabel(
            left,
            text="Welcome Administrator",
            font=("Arial", 18),
            text_color="#64748B"
        ).pack(anchor="w")

        self.time_label = ctk.CTkLabel(
            header,
            text="",
            font=("Arial", 18, "bold"),
            text_color="#334155"
        )

        self.time_label.pack(side="right")

        self.update_time()

    # =====================================
    # LIVE CLOCK
    # =====================================

    def update_time(self):

        current = datetime.now().strftime("%d-%m-%Y   %I:%M:%S %p")

        self.time_label.configure(text=current)

        self.after(1000, self.update_time)
                # ============================
        # STATISTICS CARDS
        # ============================

        cards_frame = ctk.CTkFrame(
            self.main,
            fg_color="transparent"
        )
        cards_frame.pack(fill="x", padx=30, pady=20)

        data = [
            ("Students", "120", "#2563EB"),
            ("Present", "110", "#16A34A"),
            ("Absent", "10", "#DC2626"),
            ("Attendance", "92%", "#EA580C")
        ]

        for title, value, color in data:

            card = ctk.CTkFrame(
                cards_frame,
                width=220,
                height=120,
                corner_radius=15,
                fg_color="#2E2E2E"
            )
            card.pack(side="left", padx=15)
            card.pack_propagate(False)

            ctk.CTkFrame(
                card,
                height=8,
                fg_color=color
            ).pack(fill="x")

            ctk.CTkLabel(
                card,
                text=title,
                font=("Arial",18)
            ).pack(pady=(15,5))

            ctk.CTkLabel(
                card,
                text=value,
                font=("Arial",32,"bold")
            ).pack()

        # ============================
        # QUICK ACTIONS
        # ============================

        quick = ctk.CTkFrame(
            self.main,
            fg_color="transparent"
        )
        quick.pack(fill="x", padx=30, pady=30)

        ctk.CTkLabel(
            quick,
            text="Quick Actions",
            font=("Arial",26,"bold")
        ).pack(anchor="w", pady=(0,20))

        button_frame = ctk.CTkFrame(
            quick,
            fg_color="transparent"
        )
        button_frame.pack()

        actions = [
            "Take Attendance",
            "Manage Students",
            "View Reports"
        ]

        for action in actions:

            btn = ctk.CTkButton(
                button_frame,
                text=action,
                width=220,
                height=50,
                corner_radius=10
            )
            btn.pack(side="left", padx=20)
                    # ============================
        # RECENT ACTIVITY
        # ============================

        recent_frame = ctk.CTkFrame(
            self.main,
            corner_radius=15
        )
        recent_frame.pack(fill="both", expand=True, padx=30, pady=(10, 20))

        ctk.CTkLabel(
            recent_frame,
            text="Recent Attendance",
            font=("Arial", 24, "bold")
        ).pack(anchor="w", padx=20, pady=(20, 15))

        columns = ctk.CTkFrame(
            recent_frame,
            fg_color="transparent"
        )
        columns.pack(fill="x", padx=20)

        headers = ["Student", "Time", "Status"]

        for header in headers:
            ctk.CTkLabel(
                columns,
                text=header,
                font=("Arial", 16, "bold"),
                width=200
            ).pack(side="left")

        students = [
            ("Rahul Sharma", "09:01 AM", "Present"),
            ("Anjali Patel", "09:04 AM", "Present"),
            ("Krishna", "09:08 AM", "Present"),
            ("Riya Singh", "09:10 AM", "Late"),
            ("Amit Kumar", "09:15 AM", "Present")
        ]

        for name, time, status in students:

            row = ctk.CTkFrame(
                recent_frame,
                fg_color="transparent"
            )
            row.pack(fill="x", padx=20, pady=6)

            ctk.CTkLabel(
                row,
                text=name,
                width=200
            ).pack(side="left")

            ctk.CTkLabel(
                row,
                text=time,
                width=200
            ).pack(side="left")

            color = "#16A34A"

            if status == "Late":
                color = "#EA580C"

            ctk.CTkLabel(
                row,
                text=status,
                text_color=color,
                width=200
            ).pack(side="left")

        # ============================
        # FOOTER
        # ============================

        footer = ctk.CTkLabel(
            self.main,
            text="© 2026 Biometric Attendance System | Version 1.0",
            font=("Arial", 13),
            text_color="gray"
        )
        footer.pack(side="bottom", pady=10)
