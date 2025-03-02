from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from passlib.context import CryptContext
from models import User
from typing import Annotated
from database  import engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt  # jwt needs a secret key and algorithm




# Normally we import app.get but we can make router to switch it.
router = APIRouter()

SECRET_KEY = 'd1c469fda9df2da3a9949c267c2324d69c321e881f835c55c7f39ed35b34c4e6'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated='auto')

# we need to create dependencies for each api request rely on token

oauth2_bearer  = OAuth2PasswordBearer(tokenUrl='auth/token')



class CreateUserRequest(BaseModel):
    username:str
    email:str 
    first_name:str
    last_name:str
    password:str
    role:str

class Token(BaseModel):
    access_token:str
    token_type:str

todo_router = APIRouter(
    prefix='/auth', # api start with /auth
    tags=["auth"]  # in the swagger it will be under the this tag.

)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# Depends: it is for dependency injection
db_dependency = Annotated[Session, Depends(get_db)]

def authenticate_user(username, password,db):
    user = db.query(User).filter(User.username==username).first()
    if user is None:
        print("User not found")
        return False
    if not bcrypt_context.verify(password,user.hashed_password):
        print("Password is incorrect")
        print(bcrypt_context.verify(password,user.hashed_password))
        print(password)
        print(user.hashed_password)
        return False
    return user

def create_access_token(username:str,role:str, user_id:int, expires_delta:timedelta ):
    encode ={
        'sub':username, 'id':user_id, "role":role
    }
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp':expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token:Annotated[str,Depends(oauth2_bearer)]):
    """
    We are gonna call this get_current_user first to verify the token that
    getting passed in as OAuth2 bearer token in our client call.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username:str = payload.get('sub')
        user_id:int = payload.get('id')
        user_role:str = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
        return {"username": username, "id": user_id, "user_role":user_role}
    except JWTError:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)

@router.post("/", status_code=status.HTTP_204_NO_CONTENT)
async def create_user(db: db_dependency, user_req :CreateUserRequest):
    create_user_model = User(
        email = user_req.email,
        username = user_req.username,
        first_name = user_req.first_name,
        last_name = user_req.last_name,
        role = user_req.role,
        hashed_password = bcrypt_context.hash(user_req.password),
        is_active = True
    )

    db.add(create_user_model)
    db.commit()

@router.post('/auth/token')
async def login_for_access_token(form_data:Annotated[OAuth2PasswordRequestForm, Depends()],
                                  db:db_dependency):

    user = authenticate_user(form_data.username,form_data.password, db)
    
    if not user:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    
    token = create_access_token(user.username,user.role, user.id,timedelta(minutes=20) )
    return {'access_token': token, 'token_type':'Bearer'}