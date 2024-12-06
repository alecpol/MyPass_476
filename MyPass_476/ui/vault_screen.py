import tkinter as tk
from tkinter import messagebox
from threading import Timer
from ui.base_ui import UIComponent
from backend.sensitive_data import SensitiveDataProxy

class VaultScreen(UIComponent):
    def __init__(self, root, db, session):
        super().__init__()
        self.root = root
        self.db = db
        self.session = session
        self.inactivity_timer = None

    def display(self, email):
        """Displays the user's vault."""
        self.clear_frame()
        tk.Label(self.root, text=f"Vault: {email}").grid(row=0, column=0, columnspan=4)

        # Add Buttons for Vault Actions
        tk.Button(self.root, text="Add Item", command=lambda: self.add_item(email)).grid(row=1, column=0)
        tk.Button(self.root, text="Logout", command=self.logout).grid(row=1, column=3)

        # Display Vault Items
        vault_items = self.get_vault_items(email)
        for idx, item in enumerate(vault_items):
            tk.Label(self.root, text=item['type']).grid(row=idx + 2, column=0)
            data_label = tk.Label(self.root, text=item['data'].get_data())
            data_label.grid(row=idx + 2, column=1)

            tk.Button(self.root, text="Toggle Mask", command=lambda p=item['data'], l=data_label: self.toggle_mask(p, l)).grid(row=idx + 2, column=2)
            tk.Button(self.root, text="Copy", command=lambda d=item['data']: self.copy_to_clipboard(d.get_data(unmasked=True))).grid(row=idx + 2, column=3)
            tk.Button(self.root, text="Edit", command=lambda i=item['id'], d=item['data'].get_data(unmasked=True), t=item['type']: self.edit_item(i, d, t, email)).grid(row=idx + 2, column=4)
            tk.Button(self.root, text="Delete", command=lambda i=item['id'], e=email: self.delete_item(i, e)).grid(row=idx + 2, column=5)

        self.reset_inactivity_timer()  # Start inactivity timer

    def logout(self):
        """Logs the user out and redirects to the login screen."""
        if self.inactivity_timer:
            self.inactivity_timer.cancel()  # Stop the inactivity timer
        self.mediator.notify(self, "show_login")
        messagebox.showinfo("Logout Successful", "You have been logged out successfully.")

    def add_item(self, email):
        """Opens a form to add a new vault item."""
        self.clear_frame()
        tk.Label(self.root, text="Add New Item").grid(row=0, column=0, columnspan=2)

        tk.Label(self.root, text="Type").grid(row=1, column=0)
        type_var = tk.StringVar(self.root)
        type_var.set("Login")
        type_menu = tk.OptionMenu(self.root, type_var, "Login", "Credit Card", "Identity", "Secure Notes")
        type_menu.grid(row=1, column=1)

        tk.Label(self.root, text="Data").grid(row=2, column=0)
        data_entry = tk.Entry(self.root)
        data_entry.grid(row=2, column=1)

        tk.Button(self.root, text="Save", command=lambda: self.save_item(email, type_var.get(), data_entry.get())).grid(row=3, column=0, columnspan=2)
        tk.Button(self.root, text="Cancel", command=lambda: self.display(email)).grid(row=4, column=0, columnspan=2)

    def save_item(self, email, data_type, data):
        """Saves a new item to the vault."""
        if not data.strip():
            messagebox.showwarning("Invalid Data", "Data cannot be empty.")
            return
        self.db.cursor.execute("INSERT INTO vault (user_email, data_type, data) VALUES (?, ?, ?)", (email, data_type, data))
        self.db.conn.commit()
        messagebox.showinfo("Success", "Item added successfully!")
        self.display(email)

    def edit_item(self, item_id, current_data, data_type, email):
        """Displays a form to edit an existing vault item."""
        self.clear_frame()

        tk.Label(self.root, text=f"Edit {data_type}").grid(row=0, column=0, columnspan=2)
        tk.Label(self.root, text="Data").grid(row=1, column=0)

        # Display unmasked data in the entry
        data_entry = tk.Entry(self.root, width=40)
        data_entry.insert(0, current_data)  # Insert the unmasked data
        data_entry.grid(row=1, column=1)

        # Save and Cancel Buttons
        tk.Button(self.root, text="Save", command=lambda: self.save_edit(item_id, data_entry.get(), email)).grid(row=2, column=0)
        tk.Button(self.root, text="Cancel", command=lambda: self.display(email)).grid(row=2, column=1)

    def save_edit(self, item_id, new_data, email):
        """Saves the edited item back to the vault."""
        self.db.cursor.execute("UPDATE vault SET data=? WHERE rowid=?", (new_data, item_id))
        self.db.conn.commit()
        messagebox.showinfo("Success", "Item updated successfully!")
        self.display(email)
        
    def delete_item(self, item_id, email):
        """Deletes an item from the vault."""
        self.db.cursor.execute("DELETE FROM vault WHERE rowid=?", (item_id,))
        self.db.conn.commit()
        messagebox.showinfo("Success", "Item deleted successfully!")
        self.display(email)

    def toggle_mask(self, proxy, label):
        """Toggles masking of sensitive data."""
        proxy.toggle_mask()
        label.config(text=proxy.get_data())

    def reset_inactivity_timer(self):
        """Resets the inactivity timer for auto-lock."""
        if self.inactivity_timer:
            self.inactivity_timer.cancel()
        self.inactivity_timer = Timer(300, self.auto_lock)  # Auto-lock after 5 minutes
        self.inactivity_timer.start()

    def auto_lock(self):
        """Logs the user out due to inactivity."""
        self.mediator.notify(self, "show_login")
        messagebox.showinfo("Session Locked", "Session locked due to inactivity.")

    def copy_to_clipboard(self, data):
        """Copies sensitive data to clipboard and clears it after a timeout."""
        self.root.clipboard_clear()
        self.root.clipboard_append(data)
        self.root.update()
        Timer(60, self.clear_clipboard).start()  # Clear clipboard after 1 minute

    def clear_clipboard(self):
        """Clears clipboard."""
        self.root.clipboard_clear()
        messagebox.showinfo("Clipboard Cleared", "Sensitive data cleared from clipboard.")

    def get_vault_items(self, email):
        """Retrieves all vault items for the user."""
        self.db.cursor.execute("SELECT rowid, data_type, data FROM vault WHERE user_email=?", (email,))
        return [{'id': row[0], 'type': row[1], 'data': SensitiveDataProxy(row[2])} for row in self.db.cursor.fetchall()]

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()
