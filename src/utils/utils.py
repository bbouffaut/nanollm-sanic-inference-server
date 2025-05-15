import uuid

def random_uuid() -> str:
    """Generate a random id in hexadecimal string."""
    return uuid.uuid4().hex