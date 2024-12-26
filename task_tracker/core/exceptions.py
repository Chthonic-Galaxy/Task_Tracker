# This module defines custom exception classes for the task tracker application.

class EmptyStorage(Exception):
    """Custom exception raised when the task storage is found to be empty."""
    def __init__(self, message: str = "Storage is empty.") -> None:
        """
        Initializes the EmptyStorage exception.

        Args:
            message (str): The error message. Defaults to "Storage is empty.".
        """
        super().__init__(message)

class StorageNotExists(Exception):
    """Custom exception raised when the task storage file does not exist."""
    def __init__(self, message: str = "Storage not exists.") -> None:
        """
        Initializes the StorageNotExists exception.

        Args:
            message (str): The error message. Defaults to "Storage not exists.".
        """
        super().__init__(message)