def validate_name(name):
    """check if a name is valid(not empyt, reasonable length)"""
    if not name or len(name.strip()) < 2:
        return False
    return True

def validate_email(email):
    # check if email format is valid
    if not email:
        return True #email is optional
    if "@" not in email or "." not in email:
        return False
    return True


def validate_priority(priority):
    # check if priority is valid
    valid = ["low","medium","high","critical"]
    return priority in valid

def validate_status(status):
    # check if status is valid
    valid =["active","completed","on_hold"]
    return status in valid
