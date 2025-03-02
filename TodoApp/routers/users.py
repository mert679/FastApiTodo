from fastapi import APIRouter, Path
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from models import User
from database  import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from routers.auth import get_current_user
from passlib.context import CryptContext

user_router = APIRouter(
    prefix="/user",
    tags=["user"],
)

class ChangePasswordRequset(BaseModel):
    old: str
    new_password: str
    confirm_password: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# Depends: it is for dependency injection
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[Session, Depends(get_current_user)]
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@user_router.get("/get/{user_id}")
async def get_user(user_dep:user_dependency, db:db_dependency, user_id:int = Path(gt=0)):
    if user_dep is None:
        raise HTTPException(status_code=401)
    user = db.query(User).filter(User.id == user_id).first()
    return user

@user_router.post("/change_password")
async def  change_psw(psw_req:ChangePasswordRequset, user_dep:user_dependency, db:db_dependency):
    if user_dep is None:
        raise HTTPException(status_code=401)
    db_user = db.query(User).filter(User.id == user_dep.get("id")).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not  pwd_context.verify(psw_req.old, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Old password is incorrect")

    if psw_req.new_password != psw_req.confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="New passwords do not match")

    db_user.hashed_password = pwd_context.hash(psw_req.new_password)
    db.commit()
    return {"message": "Password changed successfully"}