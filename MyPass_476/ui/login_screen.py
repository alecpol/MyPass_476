import tkinter as tk
from tkinter import messagebox
from ui.base_ui import UIComponent

class LoginScreen(UIComponent):
    def __init__(self, root, db, session):
        super().__init__()
        self.root = root
        self.db = db
        self.session = session
        self.password_visible = False

    def display(self):
        self.clear_frame()
        tk.Label(self.root, text="Email").grid(row=0, column=0)
        tk.Label(self.root, text="Password").grid(row=1, column=0)

        email_entry = tk.Entry(self.root)
        password_entry = tk.Entry(self.root, show="*")
        email_entry.grid(row=0, column=1)
        password_entry.grid(row=1, column=1)

        toggle_button = tk.Button(self.root, text="Show", command=lambda: self.toggle_password_visibility(password_entry, toggle_button))
        toggle_button.grid(row=1, column=2)

        tk.Button(self.root, text="Login", command=lambda: self.login(email_entry.get(), password_entry.get())).grid(row=2, column=0, columnspan=2)
        tk.Button(self.root, text="Register", command=lambda: self.mediator.notify(self, "show_register")).grid(row=3, column=0, columnspan=2)
        tk.Button(self.root, text="Forgot Password?", command=lambda: self.mediator.notify(self, "password_recovery")).grid(row=4, column=0, columnspan=2)

    def toggle_password_visibility(self, password_entry, toggle_button):
        if self.password_visible:
            password_entry.config(show="*")
            toggle_button.config(text="Show")
        else:
            password_entry.config(show="")
            toggle_button.config(text="Hide")
        self.password_visible = not self.password_visible

    def login(self, email, password):
        if self.db.validate_user(email, password):
            self.session.login(email)
            messagebox.showinfo("Login Success", f"Welcome {email}")
            self.mediator.notify(self, "login_success", email)
        else:
            messagebox.showerror("Login Failed", "Invalid email or password")

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()
