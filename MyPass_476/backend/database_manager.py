import sqlite3
import hashlib
import hmac

SECRET_KEY = b'super_secret_key'

class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect('mypass.db')
        self.cursor = self.conn.cursor()
        self._initialize_database()

    def _initialize_database(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            password TEXT,
            original_password TEXT,
            security_question_1 TEXT,
            security_question_2 TEXT,
            security_question_3 TEXT
        )''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS vault (
            user_email TEXT,
            data_type TEXT,
            data TEXT,
            FOREIGN KEY (user_email) REFERENCES users (email)
        )''')
        self.conn.commit()

    def original_password(self, password):
        return password

    def hash_password(self, password):
        return hmac.new(SECRET_KEY, password.encode(), hashlib.sha256).hexdigest()

    def validate_user(self, email, password):
        hashed_password = self.hash_password(password)
        self.cursor.execute('SELECT password FROM users WHERE email = ?', (email,))
        result = self.cursor.fetchone()
        return result and result[0] == hashed_password

    def add_user(self, email, password, sec_q1, sec_q2, sec_q3):
        orig_pass = self.original_password(password)
        hashed_password = self.hash_password(password)
        self.cursor.execute('INSERT INTO users (email, password, original_password, security_question_1, security_question_2, security_question_3) VALUES (?, ?, ?, ?, ?, ?)',
                            (email, hashed_password, orig_pass, sec_q1, sec_q2, sec_q3))
        self.conn.commit()
