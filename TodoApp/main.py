from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status, Path
from pydantic import BaseModel, Field
from models import Todos, Base
from database  import engine, SessionLocal
from sqlalchemy.orm import Session
from routers import auth, todos, users


app = FastAPI()

Base.metadata.create_all(bind=engine) #it creates todos.db does not exits. İf we add something it does not add something

app.include_router(auth.router)
app.include_router(todos.todo_router)
app.include_router(users.user_router)


# create db dependency
# This provides it open up request wanted but after response return it close to connection to database.



# To make post request we need to make pydantic to data validation so we are gonna create pydantic class
# class TodoRequest(BaseModel):
#     title:str = Field(min_length=3)
#     description:str = Field(max_length=100)
#     priority :int = Field(gt=0 ,lt=6)
#     complete:bool



# @app.get("/", status_code=status.HTTP_200_OK)
# async def read_all(db:db_dependency):
#     return db.query(Todos).all()

# @app.get("/todo/{Id}", status_code=status.HTTP_200_OK)
# async def read_one( db:db_dependency, Id:int =Path(gt=0)):
#     todo_model = db.query(Todos).filter(Todos.id == Id).first()
#     if todo_model is not None:
#         return todo_model
#     raise HTTPException(status_code=404, detail="Todo not found")


# @app.post("/create-todo", status_code=status.HTTP_201_CREATED)
# async def create_todo(db:db_dependency, todo_request: TodoRequest):
#     todo_model = Todos(**todo_request.model_dump())
#     db.add(todo_model)
#     db.commit()

# @app.patch("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
# async def update_todo(db:db_dependency, todo_req: TodoRequest, todo_id:int = Path(gt=0)):
#     todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
#     if todo_model is None:
#         raise HTTPException(status_code=404, detail= "Todo not found")
    
#     todo_model.title = todo_req.title
#     todo_model.description = todo_req.description
#     todo_model.priority = todo_req.priority
#     todo_model.complete = todo_req.complete
#     db.add(todo_model)
#     db.commit()

# @app.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_todo(db:db_dependency,todo_id:int = Path(gt=0)):
#     todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
#     if todo_model is None:
#         raise HTTPException(status_code=404, detail= "Todo not found")

#     db.query(Todos).filter(Todos.id == todo_id).delete()
#     db.commit()