import re

def is_valid_password(password):
    # Regex for password validation:
    pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*(),.?\":{}|<>])[A-Za-z\d!@#$%^&*(),.?\":{}|<>]{8,}$"

    if not re.match(pattern, password):
        return False, "Password must contain at least 8 characters, including one uppercase letter, one lowercase letter, one number, and one special character."

    return True, "Password is valid"