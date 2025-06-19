# db/models/test_schema/mng_user.py
from sqlalchemy import Column, Integer, String, Boolean
from app.db.database import Base

class MngUser(Base):
    __tablename__ = "mng_user"
    __table_args__ = {"schema": "test_schema"}

    rid       = Column(Integer, primary_key=True, index=True, nullable=False)   # 🔑 主キー
    username  = Column(String, unique=True, index=True, nullable=False)          # 🆔 ログインID
    password  = Column(String, nullable=False)                                   # 🔒 パスワード（ハッシュ化推奨）
    is_admin  = Column(Boolean, default=False, nullable=False)                   # 👑 管理者フラグ
