import customtkinter as ctk
import HomePage


class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__(ctk.set_appearance_mode("dark"))
        self.title("Login Page")
        self.geometry("400x520")
        self.minsize(400, 520)

        # Get the screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Position the main window in the center
        x = (screen_width / 2) - (400 / 2)
        y = (screen_height / 2) - (500 / 2)
        self.geometry(f"400x500+{int(x)}+{int(y)}")

        self.create_widgets()

    def create_widgets(self):
        # Create frames
        login_frame = ctk.CTkFrame(self)
        login_frame.pack(pady=100, padx=60, fill="both", expand=True)

        # Create labels
        title_label = ctk.CTkLabel(login_frame, text="Sign in", font=ctk.CTkFont(size=30, weight="bold"))
        title_label.pack(pady=12, padx=10)

        username_label = ctk.CTkLabel(login_frame, text="Username", font=ctk.CTkFont(size=16))
        username_label.pack(pady=0, padx=10, anchor="w")

        # Create entry fields
        self.username_entry = ctk.CTkEntry(login_frame, placeholder_text="Username")
        self.username_entry.pack(pady=6, padx=10, fill="x")

        password_label = ctk.CTkLabel(login_frame, text="Password", font=ctk.CTkFont(size=16))
        password_label.pack(pady=0, padx=10, anchor="w")

        self.password_entry = ctk.CTkEntry(login_frame, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=6, padx=10, fill="x")

        self.toggle_password_button = ctk.CTkButton(login_frame, text="Show", font=ctk.CTkFont(size=12),
                                                    command=self.toggle_password, width=60)
        self.toggle_password_button.pack(pady=6, padx=10, anchor="e")

        # Create login button
        login_button = ctk.CTkButton(login_frame, text="Sign in", font=ctk.CTkFont(size=16),
                                     command=self.login_button_callback)
        login_button.pack(pady=24, padx=10, fill="x")

    def toggle_password(self):
        if self.password_entry.cget("show") == "*":
            self.password_entry.configure(show="")
            self.toggle_password_button.configure(text="Hide")
        else:
            self.password_entry.configure(show="*")
            self.toggle_password_button.configure(text="Show")

    def show_custom_dialog(self, title, message):
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("300x150")

        # Get the dialog box dimensions
        dialog_width = 300
        dialog_height = 150

        # Get the screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Position the dialog box in the center of the screen
        dialog_x = (screen_width / 2) - (dialog_width / 2)
        dialog_y = (screen_height / 2) - (dialog_height / 2)
        dialog.geometry(f"{dialog_width}x{dialog_height}+{int(dialog_x)}+{int(dialog_y)}")


        dialog_frame = ctk.CTkFrame(dialog)
        dialog_frame.pack(pady=20, padx=20, fill="both", expand=True)

        message_label = ctk.CTkLabel(dialog_frame, text=message, font=ctk.CTkFont(size=14), wraplength=250)
        message_label.pack(pady=10)

        ok_button = ctk.CTkButton(dialog_frame, text="OK", command=dialog.destroy)
        ok_button.pack(pady=10)

        dialog.grab_set()
        self.wait_window(dialog)

    def login_button_callback(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        # Add your login logic here
        if username == "admin" and password == "123":
            self.show_custom_dialog("Success", "Login successful!")
            self.destroy()
            win = HomePage.ExpenseTracker()
            win.mainloop()
        else:
            self.show_custom_dialog("Error", "Incorrect username/password")


if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()
