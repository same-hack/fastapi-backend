# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import models                      # ✅ モデル定義を読み込む（テーブル作成のため）
from db.database import engine            # ✅ DBエンジン（接続情報）
from routers import users                 # ✅ users API のルーター読み込み

# ============================
# ✅ FastAPI アプリケーションの初期化
# ============================
app = FastAPI(
    title="My FastAPI App",              # アプリ名（Swagger上にも反映される）
    version="1.0.0",                     # バージョン
    description="Example app with Vue + FastAPI + PostgreSQL",  # 説明
)

# ============================
# ✅ CORS設定（Vueフロントエンドと通信可能に）
# ============================
# 例：http://localhost:5173 の Vue アプリからの API アクセスを許可する
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 許可するオリジン
    allow_credentials=True,
    allow_methods=["*"],                      # すべての HTTP メソッドを許可
    allow_headers=["*"],                      # すべてのヘッダーを許可
)

# ============================
# ✅ DBのテーブルを作成（初回のみ）
# ============================
# models.Base.metadata.create_all(bind=engine) を実行すると、
# ORMで定義されたすべてのテーブルがDBに作成される（既にある場合は無視）
models.Base.metadata.create_all(bind=engine)

# ============================
# ✅ APIルーター登録
# ============================
# users.router を `/api` パスにマウントする
# 結果として `/api/users/...` のようなルーティングになる
app.include_router(users.router, prefix="/api")

# 🚀 今後の拡張例：
# from routers import tasks
# app.include_router(tasks.router, prefix="/api")
