from argon2 import PasswordHasher
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.repository import AuthRepository
from app.auth.schemas import LoginRequest, TokenResponse
from app.auth.utils import create_access_token

pwd_context = PasswordHasher()


class AuthService:
    @staticmethod
    async def login(session: AsyncSession, data: LoginRequest) -> TokenResponse:
        user = await AuthRepository.get_user_by_username(session, data.username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
            )

        try:
            pwd_context.verify(user.password_hash, data.password)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
            )

        token = create_access_token(subject=str(user.id))
        return TokenResponse(access_token=token)
