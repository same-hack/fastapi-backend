from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db import models                          # ✅ モデル定義を読み込む（テーブル作成のため）
from db.database import engine                 # ✅ DBエンジン（接続情報）

from routers import users                      # ✅ users API
from routers import my_table                   # ✅ ← 追加！

# ============================
# ✅ FastAPI アプリケーションの初期化
# ============================
app = FastAPI(
    title="My FastAPI App",
    version="1.0.0",
    description="Example app with Vue + FastAPI + PostgreSQL",
)

# ============================
# ✅ CORS設定（Vueフロントエンドと通信可能に）
# ============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================
# ✅ DBのテーブルを作成（初回のみ）
# ============================
models.Base.metadata.create_all(bind=engine)

# ============================
# ✅ APIルーター登録
# ============================
app.include_router(users.router, prefix="/api")
app.include_router(my_table.router, prefix="/api")  # ✅ ← 追加！

# 🚀 今後の拡張例
# from routers import tasks
# app.include_router(tasks.router, prefix="/api")
