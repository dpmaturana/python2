# users_router.py
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from src.app.models.user import UserResponse, UserCreate, UserUpdate
from src.app.data.datasources.users_data_source import get_users_datasource, UsersDataSource

router = APIRouter(dependencies=[Depends(get_users_datasource)])
users = UsersDataSource()

@router.get("/", response_model = List[UserResponse])
def read_users():
    return users.get_all_users()

@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int):
    user = users.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate):
    new_user = users.create_user(user.dict())
    return new_user

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate):
    updated = users.update_user(user_id, user.dict())
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated

@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int):
    deleted = users.delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
