from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException, status
from jose import JWTError, jwt

from app.config import Settings

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day by default
ALGORITHM = "HS256"
SECRET_KEY = Settings.secret_key


def create_access_token(subject: str, expires_minutes: Optional[int] = None) -> str:
    expire = datetime.now() + timedelta(
        minutes=(expires_minutes or ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode = {"sub": subject, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
