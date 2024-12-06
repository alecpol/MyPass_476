import tkinter as tk
from tkinter import messagebox
from ui.base_ui import UIComponent
from backend.recovery_chain import RecoveryStep

class RecoveryScreen(UIComponent):
    def __init__(self, root, db):
        super().__init__()
        self.root = root
        self.db = db
        self.current_step = None  # Keeps track of the current step in the chain

    def start_recovery(self):
        """Initializes the recovery process."""
        self.clear_frame()

        tk.Label(self.root, text="Enter your email to begin recovery").grid(row=0, column=0, columnspan=2)
        tk.Label(self.root, text="Email").grid(row=1, column=0)

        email_entry = tk.Entry(self.root)
        email_entry.grid(row=1, column=1)

        tk.Button(self.root, text="Start Recovery", command=lambda: self.start_chain(email_entry.get())).grid(row=2, column=0, columnspan=2)

    def start_chain(self, email):
        """Starts the chain of security questions for the given email."""
        self.db.cursor.execute("SELECT security_question_1, security_question_2, security_question_3, original_password FROM users WHERE email=?", (email,))
        result = self.db.cursor.fetchone()

        if not result:
            messagebox.showerror("Error", "Email not found.")
            return

        # Parse questions and answers from stored format
        q1, a1 = result[0].split(":", 1)
        q2, a2 = result[1].split(":", 1)
        q3, a3 = result[2].split(":", 1)
        self.recovered_password = result[3]

        # Build the recovery chain
        step1 = RecoveryStep(q1, a1)
        step2 = RecoveryStep(q2, a2)
        step3 = RecoveryStep(q3, a3)

        step1.set_next(step2)
        step2.set_next(step3)

        self.current_step = step1  # Start with the first step
        self.display_current_step()

    def display_current_step(self):
        """Displays the current question in the chain."""
        self.clear_frame()

        if not self.current_step:
            messagebox.showinfo("Recovery Success", f"Your password is: {self.recovered_password}")
            self.mediator.notify(self, "show_login")
            return

        tk.Label(self.root, text=self.current_step.question).grid(row=0, column=0)
        answer_entry = tk.Entry(self.root)
        answer_entry.grid(row=0, column=1)

        tk.Button(self.root, text="Submit", command=lambda: self.validate_answer(answer_entry.get())).grid(row=1, column=0, columnspan=2)

    def validate_answer(self, answer):
        """Validates the current answer and moves to the next step if correct."""
        next_step = self.current_step.validate(answer)
        if next_step is True:  # Chain successfully completed
            messagebox.showinfo("Recovery Success", f"Your password is: {self.recovered_password}")
            self.mediator.notify(self, "show_login")
        elif next_step:  # Proceed to the next step
            self.current_step = next_step
            self.display_current_step()
        else:  # Validation failed
            messagebox.showerror("Recovery Failed", "Incorrect answer. Please try again.")

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()
