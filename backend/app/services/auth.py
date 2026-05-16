from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.services.user import UserService
from app.core.security import verify_password, create_access_token


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_service = UserService(db)

    def authenticate(self, username: str, password: str) -> tuple[str, User] | None:
        user = self.user_service.get_by_username(username)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        if user.status != 1:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is disabled")
        access_token = create_access_token(data={"sub": user.username})
        return access_token, user

    def get_current_user(self, username: str) -> User | None:
        return self.user_service.get_by_username(username)
