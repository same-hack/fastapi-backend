# ... 既存のインポートはそのまま（省略せず使ってOK）

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

# CORS設定（Vueなどのフロントエンドと接続できるようにする）
origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # フロントのURLを許可
    allow_credentials=True,
    allow_methods=["*"],    # すべてのHTTPメソッド（GET/POST/PUT/DELETE）を許可
    allow_headers=["*"],
)

# ----------------------
# モデル定義（型チェック用）
# ----------------------
class User(BaseModel):
    id: int
    name: str

class UserCreate(BaseModel):
    name: str

# ----------------------
# 仮のデータベース（リストで代用）
# ----------------------
users_db: List[User] = [
    User(id=1, name="Taro Yamada"),
    User(id=2, name="Hanako Suzuki"),
]

# ----------------------
# ユーザー一覧取得
# ----------------------
@app.get("/api/users", response_model=List[User])
def get_all_users():
    return users_db

# ----------------------
# ユーザー詳細取得（ID指定）
# ----------------------
@app.get("/api/users/{user_id}", response_model=User)
def get_user(user_id: int):
    for user in users_db:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

# ----------------------
# ユーザー追加（POST）
# ----------------------
@app.post("/api/users", response_model=User)
def create_user(user: UserCreate):
    new_id = max([u.id for u in users_db], default=0) + 1
    new_user = User(id=new_id, name=user.name)
    users_db.append(new_user)
    return new_user

# ----------------------
# ユーザー更新（PUT）
# ----------------------
@app.put("/api/users/{user_id}", response_model=User)
def update_user(user_id: int, updated_user: UserCreate):
    for user in users_db:
        if user.id == user_id:
            user.name = updated_user.name
            return user
    raise HTTPException(status_code=404, detail="User not found")

# =======================================================
# ✅ 追加: ユーザー削除（DELETE）
# =======================================================
@app.delete("/api/users/{user_id}", response_model=User)
def delete_user(user_id: int):
    # ユーザーを見つけて削除（リストからremove）
    for user in users_db:
        if user.id == user_id:
            users_db.remove(user)
            return user  # 削除されたユーザーを返す
    # 該当IDが見つからなければ 404 を返す
    raise HTTPException(status_code=404, detail="User not found")
