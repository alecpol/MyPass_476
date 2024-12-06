class UserSession:
    """Singleton pattern to manage user session securely."""
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(UserSession, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.user = None

    def login(self, username):
        self.user = username

    def logout(self):
        self.user = None
