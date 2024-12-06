from tkinter import Tk
from mediator import Mediator
from backend.database_manager import DatabaseManager
from backend.user_session import UserSession
from ui.login_screen import LoginScreen
from ui.register_screen import RegisterScreen
from ui.vault_screen import VaultScreen
from ui.recovery_screen import RecoveryScreen

if __name__ == "__main__":
    root = Tk()
    root.title("MyPass - Password Manager")
    db = DatabaseManager()
    session = UserSession()

    # Create Mediator
    mediator = Mediator()

    # Create Components
    login_screen = LoginScreen(root, db, session)
    register_screen = RegisterScreen(root, db)
    vault_screen = VaultScreen(root, db, session)
    recovery_screen = RecoveryScreen(root, db)

    # Register Components with Mediator
    mediator.register_component("login_screen", login_screen)
    mediator.register_component("register_screen", register_screen)
    mediator.register_component("vault_screen", vault_screen)
    mediator.register_component("recovery_screen", recovery_screen)

    # Start the application
    login_screen.display()
    root.mainloop()
