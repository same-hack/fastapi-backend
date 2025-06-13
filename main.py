from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db import models                          # モデル定義を読み込む（テーブル作成のため）
from db.database import engine                 # DBエンジン（接続情報）

from routers import users                      # users API
from routers import my_table                   # 追加したAPI

# ============================
# FastAPI アプリケーションの初期化
# ============================
app = FastAPI(
    title="My FastAPI App",
    version="1.0.0",
    description="Example app with Vue + FastAPI + PostgreSQL",
)

# ============================
# CORS設定（Vueフロントエンドと通信可能に）
# ============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================
# DBのテーブルを作成（初回のみ）
# DB接続失敗しても起動を継続するために例外処理を入れる
# ============================
try:
    models.Base.metadata.create_all(bind=engine)
except Exception as e:
    # ログを出して起動を続行（例：接続失敗など）
    print(f"Warning: DB接続失敗またはテーブル作成失敗: {e}")

# ============================
# APIルーター登録
# ============================
app.include_router(users.router, prefix="/api")
app.include_router(my_table.router, prefix="/api")  # 追加API

# 🚀 今後の拡張例
# from routers import tasks
# app.include_router(tasks.router, prefix="/api")
