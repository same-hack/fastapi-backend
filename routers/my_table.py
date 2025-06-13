from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import SessionLocal
from typing import List, Optional
from pydantic import BaseModel
from db.models.my_schema.my_table import MyTable


# ===============================
# ✅ レスポンス用のPydanticスキーマ
# ===============================
class MyTableResponse(BaseModel):
    rid: int
    type: int
    state: int
    datetime_update: str  # timestampはstrで受け取る（ISO形式）

    class Config:
        orm_mode = True  # ORMモデルからの自動変換を許可


# ===============================
# ✅ APIRouterインスタンスの生成
# ===============================
router = APIRouter(prefix="/my_table", tags=["MyTable"])

# ===============================
# ✅ DBセッション取得の依存関数
# ===============================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ===============================
# ✅ 全件取得APIエンドポイント
# ===============================
@router.get("/", response_model=List[MyTableResponse])
def get_all_my_table(db: Session = Depends(get_db)):
    return db.query(MyTable).all()


# ===============================
# ✅ 最新の1件取得APIエンドポイント
# ===============================
@router.get("/latest", response_model=Optional[MyTableResponse])
def get_latest_my_table(db: Session = Depends(get_db)):
    return (
        db.query(MyTable)
        .order_by(MyTable.datetime_update.desc())
        .first()
    )
