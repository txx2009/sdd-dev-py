from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import UserCreate, UserUpdate, UserPasswordUpdate, UserResponse
from app.services.user import UserService
from app.core.deps import get_current_user
from app.models.user import User
from app.core.security import hash_password, verify_password

router = APIRouter(prefix="/api/v1/users", tags=["用户"])


@router.get("", response_model=dict)
def list_users(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user_service = UserService(db)
    users, total = user_service.list_users(page, size)
    return {
        "data": [UserResponse.model_validate(u).model_dump() for u in users],
        "$page": page,
        "$size": size,
        "total": total,
    }


@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_user(
    user_create: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user_service = UserService(db)
    user = user_service.create(user_create)
    return {"data": UserResponse.model_validate(user).model_dump()}


@router.get("/{user_id}", response_model=dict)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user_service = UserService(db)
    user = user_service.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"data": UserResponse.model_validate(user).model_dump()}


@router.put("/{user_id}", response_model=dict)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user_service = UserService(db)
    user = user_service.update(user_id, user_update)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"data": UserResponse.model_validate(user).model_dump()}


@router.delete("/{user_id}", response_model=dict)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user_service = UserService(db)
    success = user_service.delete(user_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"data": None}


@router.put("/{user_id}/password", response_model=dict)
def change_password(
    user_id: int,
    password_update: UserPasswordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user_service = UserService(db)
    user = user_service.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not verify_password(password_update.old_password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Old password is incorrect")
    user.password = hash_password(password_update.new_password)
    db.commit()
    return {"data": None}
