from sqlalchemy import Column, Integer, TIMESTAMP
from db.database import Base

# ✅ my_schema.my_table に対応するモデル
class MyTable(Base):
    __tablename__ = "my_table"
    __table_args__ = {"schema": "my_schema"}  # ✅ スキーマ名を指定

    rid = Column(Integer, primary_key=True, index=True)
    type = Column(Integer)
    state = Column(Integer)
    datetime_update = Column(TIMESTAMP)
