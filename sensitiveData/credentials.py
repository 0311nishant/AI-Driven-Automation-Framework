# credentials.py

class Credentials:
    """
    A class to securely store username and password.
    
    It masks the sensitive information in its string representation to prevent
    accidental logging.
    """
    def __init__(self, username: str, password: str):
        self._username = username
        self._password = password

    def get_username(self) -> str:
        """Returns the username."""
        return self._username

    def get_password(self) -> str:
        """Returns the password."""
        return self._password
    
    def __repr__(self) -> str:
        """Masks the credentials for a safe string representation."""
        return f"Credentials(username='{self._username[:2]}...', password='***')"

