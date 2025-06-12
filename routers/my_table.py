# routers/my_table.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.my_schema.my_table import MyTable
from typing import List
from pydantic import BaseModel

# Pydantic モデル
class MyTableResponse(BaseModel):
    rid: int
    type: int
    state: int
    datetime_update: str

    class Config:
        orm_mode = True

router = APIRouter(prefix="/my_table", tags=["MyTable"])

# DBセッション依存関数
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[MyTableResponse])
def get_all_my_table(db: Session = Depends(get_db)):
    return db.query(MyTable).all()
