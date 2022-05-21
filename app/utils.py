from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_pass(password: str) -> str:
    """Hash a password for purpose of storing hashed password

    Args:
        password (str): password we want to hash

    Returns:
        str: hashed password string
    """
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    """verifies password in plain text matches hashed_password"""
    return pwd_context.verify(plain_password, hashed_password)
