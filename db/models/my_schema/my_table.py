from sqlalchemy import Column, Integer, TIMESTAMP
from sqlalchemy.orm import relationship
from db.database import Base

# ✅ my_schema.my_table に対応するモデル
class MyTable(Base):
    __tablename__ = "my_table"
    __table_args__ = {"schema": "my_schema"}  # ✅ スキーマを指定

    rid = Column(Integer, primary_key=True, index=True)
    type = Column(Integer)
    state = Column(Integer)
    datetime_update = Column(TIMESTAMP)

    # ✅ RelatedTable との一対一リレーション
    related_row = relationship(
        "models.my_schema.related_table.RelatedTable",  # ← 相手側のフルパス
        back_populates="my_table",
        uselist=False,          # 一対一のために必須
        cascade="all, delete",  # 親削除時に子も削除（必要に応じて）
    )
