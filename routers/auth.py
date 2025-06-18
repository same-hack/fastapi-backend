# routers/auth.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.database import SessionLocal
from db.models.test_schema.mng_user import MngUser
from schemas.test_schema.mng_user import LoginRequest, LoginResponse

router = APIRouter(prefix="/auth", tags=["Auth"])

def get_db():
    """DBセッションを取得し、リクエスト終了後にクローズする依存関数"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login", response_model=LoginResponse)
def login(login_req: LoginRequest, db: Session = Depends(get_db)):
    # 1) ユーザー名で検索
    user = db.query(MngUser).filter(MngUser.username == login_req.username).first()

    # 2) 存在チェック＆パスワード比較
    if not user or user.password != login_req.password:
        raise HTTPException(status_code=401, detail="ユーザー名またはパスワードが正しくありません")

    # 3) 成功レスポンス
    return {
        "rid": user.rid,
        "username": user.username,
        "is_admin": user.is_admin,
        "message": "ログイン成功",
    }
