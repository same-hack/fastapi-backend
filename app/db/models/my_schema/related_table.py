from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.database import Base

class RelatedTable(Base):
    __tablename__ = "related_table"
    __table_args__ = {"schema": "my_schema"}  # スキーマを親と揃える

    # ✅ 主キー（このテーブル独自のID）
    rid = Column(Integer, primary_key=True, index=True)

    # ✅ MyTable.rid との一対一リレーション用外部キー
    rid_mng_my_table = Column(
        Integer,
        ForeignKey("my_schema.my_table.rid"),  # スキーマ付きで指定する
        unique=True,       # ← 一対一にするために unique を付けるのが重要
        nullable=False
    )

    # ✅ 任意の datetime カラム
    date = Column(DateTime, nullable=True)

    # ✅ MyTable 側のリレーションと対応（back_populates を使って双方向に接続）
    my_table = relationship(
        "models.my_schema.my_table.MyTable",  # フルパス文字列で循環import回避
        back_populates="related_row"
    )
