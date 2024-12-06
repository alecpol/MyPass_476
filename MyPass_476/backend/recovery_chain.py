class RecoveryStep:
    """Chain of Responsibility pattern for handling security questions."""
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer
        self.next_step = None

    def set_next(self, step):
        self.next_step = step

    def validate(self, response):
        """Validates the response for the current step."""
        if response == self.answer:
            if self.next_step:
                return self.next_step  # Proceed to the next step
            return True  # End of chain; validation successful
        return False  # Validation failed
