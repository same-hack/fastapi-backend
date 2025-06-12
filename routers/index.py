# routers/index.py

from fastapi import APIRouter
from . import users

# まとめ用ルーター
api_router = APIRouter()

# /api/users を登録（prefixは users.py 側で設定済み）
api_router.include_router(users.router)
