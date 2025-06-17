# routers/index.py

from fastapi import APIRouter
from . import users
from . import upload

api_router = APIRouter()

# ユーザ系は /api/users/... になる
api_router.include_router(users.router)

# アップロードは /api/upload/... になる
api_router.include_router(upload.router)
