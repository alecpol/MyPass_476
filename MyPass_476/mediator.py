class Mediator:
    def __init__(self):
        self.components = {}

    def register_component(self, name, component):
        self.components[name] = component
        component.set_mediator(self)

    def notify(self, sender, event, *args):
        if event == "login_success":
            self.components["vault_screen"].display(*args)
        elif event == "show_login":
            self.components["login_screen"].display()
        elif event == "show_register":
            self.components["register_screen"].display()
        elif event == "password_recovery":
            self.components["recovery_screen"].start_recovery()
