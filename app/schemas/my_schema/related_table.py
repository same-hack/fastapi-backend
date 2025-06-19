# =============================
# ✅ RelatedTable 用のレスポンススキーマ定義
# =============================

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# =============================
# ✅ RelatedTable のデータ構造を定義する Pydantic スキーマ
# =============================
class RelatedTableResponse(BaseModel):
    rid: int                        # 主キー（必須）
    rid_mng_my_table: int          # 外部キー（MyTable の rid に紐づく）
    date: Optional[datetime] = None  # 任意の日時（null 可）

    class Config:
        orm_mode = True
