# db/database.py

import os  # 環境変数を取得するために必要
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ===============================================
# ✅ PostgreSQL 接続設定
# ===============================================
# 環境変数から DB 接続情報を取得して接続URLを生成
DATABASE_URL = "postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}".format(
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASSWORD"),
    host=os.environ.get("DB_HOST"),
    port=os.environ.get("DB_PORT"),
    db_name=os.environ.get("DB_NAME"),
)

# ===============================================
# ✅ SQLAlchemy エンジン（DBとの接続インターフェース）
# ===============================================
# echo=True にすると SQLがコンソールに表示される（開発中は便利）
engine = create_engine(DATABASE_URL, echo=True)

# ===============================================
# ✅ セッションローカル（DB操作に使う）
# ===============================================
# autocommit=False → 明示的に commit() が必要
# autoflush=False → flush() は必要時のみ行う
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ===============================================
# ✅ モデル定義時に継承するためのベースクラス
# ===============================================
Base = declarative_base()
