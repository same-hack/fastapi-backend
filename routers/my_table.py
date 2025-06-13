from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload  # ✅ joinedload を追加
from db.database import SessionLocal
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime  # ✅ datetime を追加
from db.models.my_schema.my_table import MyTable
from db.models.my_schema.related_table import RelatedTable  # ✅ RelatedTable を追加


# ===============================
# ✅ RelatedTable用レスポンススキーマ（追加）
# ===============================
class RelatedTableResponse(BaseModel):
    rid: int
    rid_mng_my_table: int
    date: datetime

    class Config:
        orm_mode = True


# ===============================
# ✅ レスポンス用のPydanticスキーマ
# ===============================
class MyTableResponse(BaseModel):
    rid: int
    type: int
    state: int
    datetime_update: datetime  # ✅ str → datetime（統一）

    # ✅ related_row を追加（一対一リレーション用）
    related_row: Optional[RelatedTableResponse] = None

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


# ===============================
# ✅ 最新の1件取得API（リレーション付き）
# ===============================
@router.get("/latest/with-related", response_model=Optional[MyTableResponse])
def get_latest_my_table_with_related(db: Session = Depends(get_db)):
    return (
        db.query(MyTable)
        .options(joinedload(MyTable.related_row))  # RelatedTable を同時に取得
        .order_by(MyTable.datetime_update.desc())
        .first()
    )
