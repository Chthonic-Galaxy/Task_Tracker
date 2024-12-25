class EmptyStorage(Exception):
    def __init__(self, message):
        message = message if message else "Storage is empty."
        super().__init__(message)

class StorageNotExists(Exception):
    def __init__(self, message):
        message = message if message else "Storage not exists."
        super().__init__(message)
