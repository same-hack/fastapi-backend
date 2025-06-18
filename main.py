# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db import models              # モデル定義（テーブル作成用）
from db.database import engine     # DBエンジン

from routers import users          # users API
from routers import my_table       # my_table API
from routers import upload         # upload API
from routers import auth           # auth API  ← 追加

app = FastAPI(
    title="My FastAPI App",
    version="1.0.0",
    description="Example app with Vue + FastAPI + PostgreSQL",
)

# CORS設定：Vue フロント（http://localhost:5173）からのリクエストを許可
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DBのテーブルを作成（初回のみ／失敗してもアプリ起動は継続）
try:
    models.Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Warning: DB接続失敗またはテーブル作成失敗: {e}")

# --- 既存ルーター ---

app.include_router(users.router,     prefix="/api")
app.include_router(my_table.router,  prefix="/api")
app.include_router(upload.router,    prefix="/api")
app.include_router(auth.router,      prefix="/api")

