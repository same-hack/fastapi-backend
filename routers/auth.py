from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/auth", tags=["Auth"])

# ===============================
# ✅ ダミーユーザデータ（実際はDBに置き換える予定）
# ===============================
dummy_users = [
    {"rid": 1, "username": "admin", "password": "pass", "is_admin": True},
    {"rid": 2, "username": "user", "password": "1234", "is_admin": False},
]

# ===============================
# ✅ ログインリクエスト用スキーマ
# ===============================
class LoginRequest(BaseModel):
    username: str
    password: str

# ===============================
# ✅ ログインレスポンス用スキーマ
# ===============================
class LoginResponse(BaseModel):
    rid: int
    username: str
    is_admin: bool
    message: str

# ===============================
# ✅ ログインエンドポイント
# ===============================
@router.post("/login", response_model=LoginResponse)
def login(login_req: LoginRequest):
    # ✅ 入力と一致するユーザーを探す
    for user in dummy_users:
        if user["username"] == login_req.username and user["password"] == login_req.password:
            return {
                "rid": user["rid"],
                "username": user["username"],
                "is_admin": user["is_admin"],
                "message": "ログイン成功"
            }
    # ❌ 一致しない場合はエラーを返す
    raise HTTPException(status_code=401, detail="ユーザー名またはパスワードが正しくありません")
