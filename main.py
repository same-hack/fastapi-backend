from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import users  # users.py の router を読み込む

app = FastAPI()

# フロントエンドとの接続を許可（http://localhost:5173 からのリクエストを許可）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ /api を共通プレフィックスとしてルーティング
#    これにより /api/users/... のようなルーティングになる
app.include_router(users.router, prefix="/api")
