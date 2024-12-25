class EmptyStorage(Exception):
    def __init__(self, message = "Storage is empty."):
        message = message
        super().__init__(message)

class StorageNotExists(Exception):
    def __init__(self, message = "Storage not exists."):
        message = message
        super().__init__(message)
