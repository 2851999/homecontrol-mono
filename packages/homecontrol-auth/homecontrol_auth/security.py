from typing import Any
import bcrypt
import jwt

from homecontrol_auth.exceptions import AuthenticationError


def hash_password(password: str) -> bytes:
    """Returns a hash of the given password"""

    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

def verify_password(password: str, hashed_password: bytes) -> bool:
    """Verifies whether a password matches its hash"""

    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)

def generate_jwt(payload: dict[str, Any], key: str) -> str:
    """Generates a jwt token given a payload and key"""

    return jwt.encode(payload, key, algorithm="HS256")

def verify_jwt(token: str, key: str) -> dict[str, Any]:
    """Verifies whether a jwt is valid and returns its payload"""

    try:
        return jwt.decode(jwt=token, key=key, algorithms=["HS256"])
    except jwt.exceptions.ExpiredSignatureError:
        raise AuthenticationError("Token has expired")
