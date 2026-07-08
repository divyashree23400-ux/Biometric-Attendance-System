import customtkinter as ctk


class SettingsPage(ctk.CTkFrame):

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

            if menu == "⚙ Settings":
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

        # Logout Button

        ctk.CTkButton(
            self.sidebar,
            text="Logout",
            fg_color="red",
            hover_color="#8B0000",
            height=45
        ).pack(side="bottom", fill="x", padx=18, pady=20)

        # =====================================
        # MAIN AREA
        # =====================================

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

        # =====================================
        # HEADER
        # =====================================

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
            text="Settings",
            font=("Arial",34,"bold"),
            text_color="#1E293B"
        ).pack(anchor="w")

        ctk.CTkLabel(
            left,
            text="Manage Application Preferences",
            font=("Arial",18),
            text_color="#64748B"
        ).pack(anchor="w")

        # =====================================
        # CONTENT
        # =====================================

        container = ctk.CTkFrame(
            self.main,
            fg_color="transparent"
        )

        container.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0,20)
        )

        # Left Panel

        self.left = ctk.CTkFrame(
            container,
            width=360,
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
            container,
            corner_radius=15
        )

        self.right.pack(
            side="right",
            fill="both",
            expand=True
        )

        # Build UI

        self.create_admin_settings()
        self.create_system_settings()
            # =====================================
    # ADMIN SETTINGS
    # =====================================

    def create_admin_settings(self):

        ctk.CTkLabel(
            self.left,
            text="Administrator Profile",
            font=("Arial",24,"bold")
        ).pack(pady=(20,20))

        # -----------------------------
        # Administrator Name
        # -----------------------------

        ctk.CTkLabel(
            self.left,
            text="Administrator Name",
            font=("Arial",15,"bold")
        ).pack(anchor="w", padx=20)

        self.admin_name = ctk.CTkEntry(
            self.left,
            width=300,
            height=40,
            placeholder_text="Administrator Name"
        )
        self.admin_name.pack(pady=(5,15))
        self.admin_name.insert(0, "Admin")

        # -----------------------------
        # Email
        # -----------------------------

        ctk.CTkLabel(
            self.left,
            text="Email Address",
            font=("Arial",15,"bold")
        ).pack(anchor="w", padx=20)

        self.email = ctk.CTkEntry(
            self.left,
            width=300,
            height=40,
            placeholder_text="Email Address"
        )
        self.email.pack(pady=(5,15))
        self.email.insert(0, "admin@gmail.com")

        # -----------------------------
        # Phone Number
        # -----------------------------

        ctk.CTkLabel(
            self.left,
            text="Phone Number",
            font=("Arial",15,"bold")
        ).pack(anchor="w", padx=20)

        self.phone = ctk.CTkEntry(
            self.left,
            width=300,
            height=40,
            placeholder_text="Phone Number"
        )
        self.phone.pack(pady=(5,15))
        self.phone.insert(0, "9876543210")

        # -----------------------------
        # Password
        # -----------------------------

        ctk.CTkLabel(
            self.left,
            text="Change Password",
            font=("Arial",15,"bold")
        ).pack(anchor="w", padx=20)

        self.password = ctk.CTkEntry(
            self.left,
            width=300,
            height=40,
            show="*",
            placeholder_text="New Password"
        )
        self.password.pack(pady=(5,20))

        # -----------------------------
        # Buttons
        # -----------------------------

        ctk.CTkButton(
            self.left,
            text="💾 Save Profile",
            width=300,
            height=45,
            fg_color="#2563EB",
            hover_color="#1D4ED8"
        ).pack(pady=8)

        ctk.CTkButton(
            self.left,
            text="🔄 Reset",
            width=300,
            height=45,
            fg_color="#64748B",
            hover_color="#475569"
        ).pack(pady=8)
            # =====================================
    # SYSTEM SETTINGS
    # =====================================

    def create_system_settings(self):

        ctk.CTkLabel(
            self.right,
            text="System Settings",
            font=("Arial",24,"bold")
        ).pack(anchor="w", padx=25, pady=(20,20))

        # =====================================
        # Appearance
        # =====================================

        appearance = ctk.CTkFrame(
            self.right,
            corner_radius=15
        )
        appearance.pack(fill="x", padx=25, pady=10)

        ctk.CTkLabel(
            appearance,
            text="Appearance",
            font=("Arial",18,"bold")
        ).pack(anchor="w", padx=20, pady=(15,10))

        self.theme = ctk.CTkComboBox(
            appearance,
            width=250,
            values=[
                "System",
                "Light",
                "Dark"
            ]
        )
        self.theme.set("System")
        self.theme.pack(anchor="w", padx=20, pady=(0,15))

        # =====================================
        # Camera Settings
        # =====================================

        camera = ctk.CTkFrame(
            self.right,
            corner_radius=15
        )
        camera.pack(fill="x", padx=25, pady=10)

        ctk.CTkLabel(
            camera,
            text="Camera Settings",
            font=("Arial",18,"bold")
        ).pack(anchor="w", padx=20, pady=(15,10))

        self.camera = ctk.CTkComboBox(
            camera,
            width=250,
            values=[
                "Default Camera",
                "USB Camera",
                "External Webcam"
            ]
        )
        self.camera.set("Default Camera")
        self.camera.pack(anchor="w", padx=20, pady=(0,15))

        # =====================================
        # Notification Settings
        # =====================================

        notification = ctk.CTkFrame(
            self.right,
            corner_radius=15
        )
        notification.pack(fill="x", padx=25, pady=10)

        ctk.CTkLabel(
            notification,
            text="Notifications",
            font=("Arial",18,"bold")
        ).pack(anchor="w", padx=20, pady=(15,10))

        self.email_notify = ctk.CTkCheckBox(
            notification,
            text="Enable Email Notifications"
        )
        self.email_notify.pack(anchor="w", padx=20)

        self.sound_notify = ctk.CTkCheckBox(
            notification,
            text="Enable Sound Alerts"
        )
        self.sound_notify.pack(anchor="w", padx=20)

        self.auto_backup = ctk.CTkCheckBox(
            notification,
            text="Enable Automatic Backup"
        )
        self.auto_backup.pack(anchor="w", padx=20, pady=(0,15))

        # =====================================
        # Attendance Settings
        # =====================================

        attendance = ctk.CTkFrame(
            self.right,
            corner_radius=15
        )
        attendance.pack(fill="x", padx=25, pady=10)

        ctk.CTkLabel(
            attendance,
            text="Attendance Settings",
            font=("Arial",18,"bold")
        ).pack(anchor="w", padx=20, pady=(15,10))

        self.late_time = ctk.CTkEntry(
            attendance,
            width=250,
            placeholder_text="Late Time (Minutes)"
        )
        self.late_time.pack(anchor="w", padx=20, pady=(0,10))
        self.late_time.insert(0, "10")

        self.threshold = ctk.CTkEntry(
            attendance,
            width=250,
            placeholder_text="Face Recognition Threshold"
        )
        self.threshold.pack(anchor="w", padx=20, pady=(0,15))
        self.threshold.insert(0, "0.75")

        # =====================================
        # Action Buttons
        # =====================================

        buttons = ctk.CTkFrame(
            self.right,
            fg_color="transparent"
        )
        buttons.pack(pady=30)

        ctk.CTkButton(
            buttons,
            text="💾 Save Settings",
            width=180,
            height=45,
            fg_color="#2563EB",
            hover_color="#1D4ED8"
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            buttons,
            text="🔄 Reset",
            width=180,
            height=45,
            fg_color="#64748B",
            hover_color="#475569"
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            buttons,
            text="🗑 Restore Defaults",
            width=180,
            height=45,
            fg_color="#DC2626",
            hover_color="#B91C1C"
        ).pack(side="left", padx=10)
        