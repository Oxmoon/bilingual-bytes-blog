from password_strength import PasswordPolicy, PasswordStats
from password_strength.tests import Length, Numbers, Uppercase

policy = PasswordPolicy.from_names(length=8, uppercase=1, numbers=1)


def validate_policy(password):
    tested_pass = policy.password(password)
    errors = tested_pass.test()
    if len(errors) > 0:
        if isinstance(errors[0], Length):
            return "Password must be at least 8 characters long."
        if isinstance(errors[0], Uppercase):
            return "Password must contain at least 1 uppercase character."
        if isinstance(errors[0], Numbers):
            return "Password must contain at least 1 number."
    if tested_pass.strength() < 0.3:
        return "Avoid using consecutive characters and easy to guess words."


def validate_strength(password):
    stats = PasswordStats(password).strength()
    if stats >= 0.8:
        return "Very Strong"
    if stats >= 0.65:
        return "Strong"
    if stats >= 0.5:
        return "Okay"
    if stats >= 0.3:
        return "Weak"
    return "Poor"
