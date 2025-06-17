from sqlalchemy import Column, Integer, TIMESTAMP
from sqlalchemy.orm import relationship
from db.database import Base

# ✅ my_schema.my_table に対応するモデル
class MyTable(Base):
    __tablename__ = "my_table"
    __table_args__ = {"schema": "my_schema"}  # ✅ スキーマを指定

    # 🔑 主キー：必須
    rid = Column(Integer, primary_key=True, index=True, nullable=False)

    # ✅ 種別：必須
    type = Column(Integer, nullable=False)

    # ✅ 状態：任意（null許容）
    state = Column(Integer, nullable=True)

    # ✅ 最終更新日時：任意（null許容）
    datetime_update = Column(TIMESTAMP, nullable=True)

    # 🔗 RelatedTable との一対一リレーション
    related_row = relationship(
        "models.my_schema.related_table.RelatedTable",  # ← 相手側のフルパス
        back_populates="my_table",
        uselist=False,          # 一対一のために必須
        cascade="all, delete",  # 親削除時に子も削除（必要に応じて）
    )
