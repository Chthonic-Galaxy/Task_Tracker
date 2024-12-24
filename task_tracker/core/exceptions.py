class EmptyStorage(Exception):
    def __init__(self, message):
        message = message if message else "Storage is empty."
        super().__init__(message)
