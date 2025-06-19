# schemas/test_schema/mng_user.py

from pydantic import BaseModel
from typing import Optional

# ==========================
# 🔐 ログインリクエスト用
# ==========================
class LoginRequest(BaseModel):
    username: str  # 🔑 ログインID
    password: str  # 🔒 パスワード

# ==========================
# ✅ ログイン成功時のレスポンス
# ==========================
class LoginResponse(BaseModel):
    rid: int
    username: str
    is_admin: bool
    message: str

    class Config:
        from_attributes = True  # 🛠 ORMモデルからの自動変換を許可

# ==========================
# 🔑 JWTトークン付きレスポンス（API返却用）
# ==========================
class TokenResponse(BaseModel):
    access_token: str  # 🪪 JWTアクセストークン
    token_type: str    # 一般的に "bearer"
    rid: int           # ユーザーID
    username: str      # ユーザー名
    is_admin: bool     # 管理者フラグ
    message: str       # 成功メッセージ
