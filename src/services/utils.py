import re

from src.exceptions import InvalidCharacterException


class Validator:
    @staticmethod
    def validate_string(strin: str):
        """Takes one positional argument.
        Checks if the string contains any
        forbidden characters."""
        if not re.match(r"^[a-zA-Z0-9. ]+$", strin):
            raise InvalidCharacterException
        return strin
