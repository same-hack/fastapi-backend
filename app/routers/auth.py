# routers/auth.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models.test_schema.mng_user import MngUser
from app.schemas.test_schema.mng_user import LoginRequest, LoginResponse, TokenResponse
from jose import JWTError, jwt
from datetime import datetime, timedelta

# 認証用ルーターの定義
router = APIRouter(prefix="/auth", tags=["Auth"])

# ====================================
# JWT設定（開発中のため仮のシークレットキーを使用）
# ====================================
SECRET_KEY = "your-secret-key"  # 本番環境では環境変数などで管理する
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # トークンの有効期限（分）

# ====================================
# DBセッション取得関数
# ====================================
def get_db():
    """リクエストごとにDBセッションを取得し、終了時にクローズする"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ====================================
# JWTトークンの作成関数
# ====================================
def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    JWTアクセストークンを生成し、署名して返す。
    `data` にはユーザー情報（例: ユーザーID）を含める。
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})  # 有効期限をトークンに含める
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# ====================================
# ログインエンドポイント
# ====================================
@router.post("/login", response_model=TokenResponse)
def login(login_req: LoginRequest, db: Session = Depends(get_db)):
    """
    ユーザー名とパスワードを検証し、正しければJWTトークンを発行。
    現在は開発中のため、パスワードはプレーンテキストでDBに保存されている前提。
    """
    # ユーザーをDBから取得
    user = db.query(MngUser).filter(MngUser.username == login_req.username).first()

    # ユーザーの存在とパスワードの一致を確認（ハッシュ化していない前提）
    if not user or user.password != login_req.password:
        raise HTTPException(status_code=401, detail="ユーザー名またはパスワードが正しくありません")

    # JWTトークンのペイロードには、ユーザーIDなどの一意な情報を含める
    token_data = {"sub": str(user.rid)}
    access_token = create_access_token(data=token_data)

    # 成功レスポンスとしてJWTとユーザー情報を返却
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        rid=user.rid,
        username=user.username,
        is_admin=user.is_admin,
        message="ログイン成功"
    )
