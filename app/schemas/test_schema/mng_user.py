# schemas/test_schema/mng_user.py
from pydantic import BaseModel
from typing import Optional

class LoginRequest(BaseModel):
    username: str  # 🔑 ログインID
    password: str  # 🔒 パスワード

class LoginResponse(BaseModel):
    rid: int
    username: str
    is_admin: bool
    message: str

    class Config:
        from_attributes = True  # 🛠 ORMモデルからの自動変換を許可
