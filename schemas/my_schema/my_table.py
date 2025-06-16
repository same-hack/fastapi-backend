# =============================
# ✅ MyTable 用のレスポンススキーマ定義
# =============================

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# 🔄 関連テーブルのスキーマも取り込む（リレーションで使用）
from .related_table import RelatedTableResponse


# =============================
# ✅ MyTable のデータ構造を定義する Pydantic スキーマ
# =============================
class MyTableResponse(BaseModel):
    rid: int                  # 主キー（必須）
    type: int                 # 任意の種別（例：1 = Aタイプ, 2 = Bタイプ）
    state: int                # 任意の状態（例：0 = 未処理, 1 = 処理済み）
    datetime_update: datetime # 最終更新日時

    # 🔗 リレーション：related_row という名前で RelatedTable と接続
    related_row: Optional[RelatedTableResponse] = None

    # ✅ ORM モデルからの変換を許可（FastAPI の自動変換で必要）
    class Config:
        orm_mode = True
