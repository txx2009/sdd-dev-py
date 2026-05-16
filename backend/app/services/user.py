from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import hash_password


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_by_username(self, username: str) -> User | None:
        return self.db.query(User).filter(User.username == username).first()

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def list_users(self, page: int = 1, size: int = 10) -> tuple[list[User], int]:
        query = self.db.query(User)
        total = query.count()
        users = query.offset((page - 1) * size).limit(size).all()
        return users, total

    def create(self, user_create: UserCreate) -> User:
        user = User(
            username=user_create.username,
            password=hash_password(user_create.password),
            nickname=user_create.nickname,
            email=user_create.email,
            phone=user_create.phone,
            status=user_create.status,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user_id: int, user_update: UserUpdate) -> User | None:
        user = self.get_by_id(user_id)
        if not user:
            return None
        update_data = user_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user_id: int) -> bool:
        user = self.get_by_id(user_id)
        if not user:
            return False
        self.db.delete(user)
        self.db.commit()
        return True
