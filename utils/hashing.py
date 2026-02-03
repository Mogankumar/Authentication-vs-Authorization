import bcrypt

def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def verify_password(raw_password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(raw_password.encode(), hashed_password)
