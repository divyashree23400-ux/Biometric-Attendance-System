import customtkinter as ctk
from tkinter import messagebox


class LoginPage(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.master = master
        self.pack(fill="both", expand=True)

        # =====================================
        # LEFT PANEL
    
        # =====================================
        left_frame = ctk.CTkFrame(
            self,
            width=350,
            corner_radius=0
        )
        left_frame.pack(side="left", fill="y")
        left_frame.pack_propagate(False)

        title = ctk.CTkLabel(
            left_frame,
            text="BIOMETRIC\nATTENDANCE\nSYSTEM",
            font=("Arial", 28, "bold"),
            justify="center"
        )
        title.pack(pady=(120, 20))

        subtitle = ctk.CTkLabel(
            left_frame,
            text="Secure • Smart • Cloud Based",
            font=("Arial", 16)
        )
        subtitle.pack()

        # =====================================
        # RIGHT PANEL
        # =====================================
        right_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        right_frame.pack(
            side="right",
            fill="both",
            expand=True
        )

        heading = ctk.CTkLabel(
            right_frame,
            text="Welcome Back!",
            font=("Arial", 30, "bold")
        )
        heading.pack(pady=(70, 5))

        subheading = ctk.CTkLabel(
            right_frame,
            text="Administrator Login",
            font=("Arial", 18)
        )
        subheading.pack(pady=(0, 30))

        self.username = ctk.CTkEntry(
            right_frame,
            width=320,
            height=40,
            placeholder_text="Username"
        )
        self.username.pack(pady=10)

        self.password = ctk.CTkEntry(
            right_frame,
            width=320,
            height=40,
            placeholder_text="Password",
            show="*"
        )
        self.password.pack(pady=10)

        self.remember = ctk.CTkCheckBox(
            right_frame,
            text="Remember Me"
        )
        self.remember.pack(anchor="w", padx=210, pady=5)

        forgot = ctk.CTkButton(
            right_frame,
            text="Forgot Password?",
            fg_color="transparent",
            hover=False,
            text_color="#4EA8FF",
            command=self.forgot_password
        )
        forgot.pack(pady=(0, 20))

        login_btn = ctk.CTkButton(
            right_frame,
            text="LOGIN",
            width=320,
            height=40,
            command=self.login
        )
        login_btn.pack(pady=10)

        exit_btn = ctk.CTkButton(
            right_frame,
            text="EXIT",
            width=320,
            height=40,
            fg_color="red",
            hover_color="#990000",
            command=self.master.destroy
        )
        exit_btn.pack(pady=10)

        footer = ctk.CTkLabel(
            right_frame,
            text="Version 1.0\n© 2026 Biometric Attendance System",
            font=("Arial", 12)
        )
        footer.pack(side="bottom", pady=20)

    # =====================================
    # LOGIN FUNCTION
    # =====================================
    def login(self):

        username = self.username.get()
        password = self.password.get()

        if username == "admin" and password == "admin123":
            messagebox.showinfo(
                "Success",
                "Login Successful!"
            )
        else:
            messagebox.showerror(
                "Error",
                "Invalid Username or Password"
            )

    # =====================================
    # FORGOT PASSWORD
    # =====================================
    def forgot_password(self):

        messagebox.showinfo(
            "Forgot Password",
            "Please contact the administrator\nor reset your password through Firebase."
        )