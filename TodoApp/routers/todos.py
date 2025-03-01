from fastapi import APIRouter, Depends, HTTPException, Path, status

from pydantic import BaseModel,Field
from models import Todos
from typing import Annotated
from database  import engine, SessionLocal
from sqlalchemy.orm import Session
from routers.auth import get_current_user


todo_router = APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# Depends: it is for dependency injection
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class TodoRequest(BaseModel):
    title:str = Field(min_length=3)
    description:str = Field(max_length=100)
    priority :int = Field(gt=0 ,lt=6)
    complete:bool

@todo_router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user:user_dependency,   db:db_dependency):
    if user is None:
        raise HTTPException(status_code=401)
    return db.query(Todos).filter(Todos.owner_id == user.get("id")).all()

@todo_router.get("/todo/{Id}", status_code=status.HTTP_200_OK)
async def read_one( user:user_dependency, db:db_dependency, Id:int =Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401)
    todo_model = db.query(Todos).filter(Todos.id == Id).filter(Todos.owner_id == user.get("id")).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found")


@todo_router.post("/create-todo", status_code=status.HTTP_201_CREATED)
async def create_todo(user:user_dependency,db:db_dependency, todo_request: TodoRequest):
    print("user")
    if user is None:
        raise HTTPException(status_code=401)
    
    todo_model = Todos(**todo_request.model_dump(), owner_id=user.get("id"))
    
    db.add(todo_model)
    db.commit()

@todo_router.patch("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db:db_dependency, todo_req: TodoRequest, todo_id:int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail= "Todo not found")
    
    todo_model.title = todo_req.title
    todo_model.description = todo_req.description
    todo_model.priority = todo_req.priority
    todo_model.complete = todo_req.complete
    db.add(todo_model)
    db.commit()

@todo_router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db:db_dependency,todo_id:int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail= "Todo not found")

    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()