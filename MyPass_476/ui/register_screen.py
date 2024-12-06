import tkinter as tk
from tkinter import messagebox
from ui.base_ui import UIComponent
from backend.password_builder import PasswordBuilder
from backend.event_manager import EventManager, UserNotification


class RegisterScreen(UIComponent):
    def __init__(self, root, db):
        super().__init__()
        self.root = root
        self.db = db
        self.password_visible = False

        # Initialize EventManager and Observer
        self.event_manager = EventManager()
        self.user_notification = UserNotification()
        self.event_manager.register_observer(self.user_notification)

    def display(self):
        """Displays the registration form."""
        self.clear_frame()
        tk.Label(self.root, text="Register an Account").grid(row=0, column=0, columnspan=2)

        tk.Label(self.root, text="Email").grid(row=1, column=0)
        email_entry = tk.Entry(self.root)
        email_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Password").grid(row=2, column=0)
        password_entry = tk.Entry(self.root, show="*")
        password_entry.grid(row=2, column=1)

        toggle_button = tk.Button(self.root, text="Show", command=lambda: self.toggle_password_visibility(password_entry, toggle_button))
        toggle_button.grid(row=2, column=2)

        # Predefined Security Questions
        questions = [
            "What is your pet's name?",
            "What is your favorite color?",
            "What city were you born in?",
            "What is your mother's maiden name?",
            "What is the name of your first school?",
        ]

        # Security Question 1
        tk.Label(self.root, text="Security Question 1").grid(row=3, column=0)
        question1_var = tk.StringVar(self.root)
        question1_var.set(questions[0])
        question1_menu = tk.OptionMenu(self.root, question1_var, *questions)
        question1_menu.grid(row=3, column=1)
        answer1_entry = tk.Entry(self.root)
        answer1_entry.grid(row=3, column=2)

        # Security Question 2
        tk.Label(self.root, text="Security Question 2").grid(row=4, column=0)
        question2_var = tk.StringVar(self.root)
        question2_var.set(questions[1])
        question2_menu = tk.OptionMenu(self.root, question2_var, *questions)
        question2_menu.grid(row=4, column=1)
        answer2_entry = tk.Entry(self.root)
        answer2_entry.grid(row=4, column=2)

        # Security Question 3
        tk.Label(self.root, text="Security Question 3").grid(row=5, column=0)
        question3_var = tk.StringVar(self.root)
        question3_var.set(questions[2])
        question3_menu = tk.OptionMenu(self.root, question3_var, *questions)
        question3_menu.grid(row=5, column=1)
        answer3_entry = tk.Entry(self.root)
        answer3_entry.grid(row=5, column=2)

        tk.Button(self.root, text="Generate Password", command=lambda: self.generate_password(password_entry)).grid(row=6, column=0, columnspan=2)
        tk.Button(self.root, text="Register", command=lambda: self.register(
            email_entry.get(), password_entry.get(),
            question1_var.get(), answer1_entry.get(),
            question2_var.get(), answer2_entry.get(),
            question3_var.get(), answer3_entry.get()
        )).grid(row=7, column=0, columnspan=3)

    def toggle_password_visibility(self, password_entry, toggle_button):
        """Toggles password visibility."""
        if self.password_visible:
            password_entry.config(show="*")
            toggle_button.config(text="Show")
        else:
            password_entry.config(show="")
            toggle_button.config(text="Hide")
        self.password_visible = not self.password_visible

    def generate_password(self, password_entry):
        """Generates a strong password and fills the password field."""
        builder = PasswordBuilder()
        password = builder.set_length(12).include_uppercase().include_digits().include_special_characters().build()
        password_entry.delete(0, tk.END)
        password_entry.insert(0, password)

    def register(self, email, password, question1, answer1, question2, answer2, question3, answer3):
        """Handles user registration."""
        if len(password) < 8:
            self.event_manager.notify("Weak password detected.")
            messagebox.showwarning("Weak Password", "Password must be at least 8 characters long!")
            return

        # Ensure all questions and answers are provided
        if not all([question1, answer1, question2, answer2, question3, answer3]):
            messagebox.showerror("Error", "All security questions and answers must be filled out.")
            return

        # Save the questions and answers separately in the database
        self.db.add_user(email, password, f"{question1}:{answer1}", f"{question2}:{answer2}", f"{question3}:{answer3}")
        messagebox.showinfo("Registration Success", "Account registered successfully!")
        self.mediator.notify(self, "show_login")


    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()
