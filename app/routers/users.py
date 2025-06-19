from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

# ✅ "/users" をプレフィックスとするAPIグループを作成
router = APIRouter(prefix="/users", tags=["Users"])

# --- モデル定義 ---
class User(BaseModel):
    id: int
    name: str

class UserCreate(BaseModel):
    name: str

# --- 仮のデータベース ---
users_db: List[User] = [
    User(id=1, name="Taro Yamada"),
    User(id=2, name="Hanako Suzuki"),
]

# --- ユーザー一覧取得 ---
@router.get("/", response_model=List[User])
def get_all_users():
    return users_db

# --- ユーザー詳細取得 ---
@router.get("/{user_id}", response_model=User)
def get_user(user_id: int):
    for user in users_db:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

# --- ユーザー追加 ---
@router.post("/", response_model=User)
def create_user(user: UserCreate):
    new_id = max([u.id for u in users_db], default=0) + 1
    new_user = User(id=new_id, name=user.name)
    users_db.append(new_user)
    return new_user

# --- ユーザー更新 ---
@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, updated_user: UserCreate):
    for user in users_db:
        if user.id == user_id:
            user.name = updated_user.name
            return user
    raise HTTPException(status_code=404, detail="User not found")

# --- ユーザー削除 ---
@router.delete("/{user_id}", response_model=User)
def delete_user(user_id: int):
    for user in users_db:
        if user.id == user_id:
            users_db.remove(user)
            return user
    raise HTTPException(status_code=404, detail="User not found")
