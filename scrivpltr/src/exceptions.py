# exceptions.py

class ScrivenerError(Exception):
    """Base class for all Scrivener-related errors."""
    pass

class FileNotFoundError(ScrivenerError):
    """Exception raised when the provided file is not found."""
    def __init__(self, file_path):
        super().__init__(f"The provided file path does not exist: {file_path}")

class InvalidFileTypeError(ScrivenerError):
    """Exception raised when the provided file is not a valid .scrivx file."""
    def __init__(self, file_path):
        super().__init__(f"The provided file is not a valid .scrivx file: {file_path}")

class InvalidScrivenerVersionError(ScrivenerError):
    """Exception raised when the Scrivener version is not supported."""
    def __init__(self, version):
        super().__init__(f"This does not appear to be a Scrivener 3 file (version 2.0 required, got {version})")

class NotAFileError(ScrivenerError):
    """Exception raised when the provided path is not a file."""
    def __init__(self, path):
        super().__init__(f"The provided path is not a valid file: {path}")
