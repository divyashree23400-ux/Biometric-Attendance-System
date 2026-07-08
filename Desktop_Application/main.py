import customtkinter as ctk

# Import Pages
from pages.dashboard import Dashboard
from pages.students import StudentsPage
from pages.attendance import AttendancePage
from pages.reports import ReportsPage
from pages.settings import SettingsPage


class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Biometric Attendance System")
        self.geometry("1600x900")
        self.minsize(1400, 800)

        # ============================
        # CHANGE THIS TO OPEN ANY PAGE
        # Uncomment ONLY ONE page at a time
        # ============================

        # Dashboard(self)
        StudentsPage(self)
        # AttendancePage(self)
        # ReportsPage(self)
        # SettingsPage(self)


if __name__ == "__main__":

    ctk.set_appearance_mode("Light")
    ctk.set_default_color_theme("blue")

    app = App()
    app.mainloop()