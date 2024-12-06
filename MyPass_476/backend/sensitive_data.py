class SensitiveDataProxy:
    """Proxy pattern to mask and unmask sensitive data."""
    def __init__(self, data):
        self._data = data
        self._masked = True

    def toggle_mask(self):
        """Toggles between masked and unmasked states."""
        self._masked = not self._masked

    def get_data(self, unmasked=False):
        """Returns the data, masked or unmasked based on the state."""
        if unmasked or not self._masked:
            return self._data
        return "****"
