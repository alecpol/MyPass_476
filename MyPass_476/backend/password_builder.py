import random
import string

class PasswordBuilder:
    def __init__(self):
        self.length = 8
        self._include_upper = False
        self._include_digits = False
        self._include_special = False

    def set_length(self, length):
        self.length = length
        return self

    def include_uppercase(self):
        self._include_upper = True
        return self

    def include_digits(self):
        self._include_digits = True
        return self

    def include_special_characters(self):
        self._include_special = True
        return self

    def build(self):
        characters = string.ascii_lowercase
        if self._include_upper:
            characters += string.ascii_uppercase
        if self._include_digits:
            characters += string.digits
        if self._include_special:
            characters += "!@#$%^&*()"

        if len(characters) == 0:
            raise ValueError("Password must include at least one character type")

        return ''.join(random.choice(characters) for _ in range(self.length))
