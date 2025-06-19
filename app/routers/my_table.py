from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload
from app.db.database import SessionLocal
from typing import List, Optional

# ✅ スキーマ（Pydanticモデル）は外部ファイルからインポート
from app.schemas.my_schema.my_table import MyTableResponse
from app.db.models.my_schema.my_table import MyTable

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
        app.db.close()

# ===============================
# ✅ 全件取得APIエンドポイント
# ===============================
@router.get("/", response_model=List[MyTableResponse])
def get_all_my_table(db: Session = Depends(get_db)):
    # 🚀 RelatedTable も同時に取得（リレーション込み）
    return (
        app.db.query(MyTable)
        .options(joinedload(MyTable.related_row))
        .all()
    )

# ===============================
# ✅ 最新の1件取得APIエンドポイント（ridベース）
# ===============================
@router.get("/latest", response_model=Optional[MyTableResponse])
def get_latest_my_table(db: Session = Depends(get_db)):
    return (
        app.db.query(MyTable)
        .order_by(MyTable.rid.desc())  # ✅ rid を基準に降順で並べて最初の1件
        .first()
    )

# ===============================
# ✅ 最新の1件取得API（リレーション付き、ridベース）
# ===============================
@router.get("/latest/with-related", response_model=Optional[MyTableResponse])
def get_latest_my_table_with_related(db: Session = Depends(get_db)):
    return (
        app.db.query(MyTable)
        .options(joinedload(MyTable.related_row))  # RelatedTable を同時に取得
        .order_by(MyTable.rid.desc())              # ✅ ridベースに変更
        .first()
    )