# db/models/__init__.py

# まず Base を database.py から持ってくる
from db.database import Base

# 次に各テーブルモデルをインポート
from .my_schema.my_table import MyTable

# __all__ で外部に見せる名前を宣言（任意）
__all__ = ["Base", "MyTable"]
