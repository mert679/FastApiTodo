# This is guide to learn FastAPI. Notes for needs.

## content
### How to run fastapi development server
There are few methods to run fastapi development server. However, we are gonna use most used one which is the uvicorn server. How to run this server first we need to download uvicorn.
After download uvicorn:
1) uvicorn main:app --reload  #which means main.py file has variable name app which is equal to FastApi
2) uvicorn main:app --host 127.0.0.1 --port 8080 --reload #special Ip and port
3) uvicorn main:app --host 0.0.0.0 --port 8080 --workers 4 # run Production environment we need to turn of --reload into production environment.   4 işlemci çekirdeği kullanır, böylece çoklu istekleri daha verimli işleyebilir.

### main.py how to define something what we made it in here.
In this py file we define the FastApi module here. and we setup some settings.
- we define FastAPI() module here.
- app.include_router() we add route in here.
- Base.metadata.create_all(bind=engine) #Bu kod todos.db dosyası yoksa oluşturuyor, ancak eğer zaten varsa var olan yapıyı değiştirmiyor. Yeni tablolar eklediğinde veya var olanları değiştirdiğinde değişiklikler otomatik olarak uygulanmaz.
- ALLOWED_HOSTS usage:
    - Varsayılan olarak FastAPI sadece localhost üzerinden çalışır. Eğer dış dünyaya açmak istiyorsan CORS ayarlarını yapmalısın.
    - ```python
        from fastapi.middleware.cors import CORSMiddleware

        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Tüm domainlerden erişim sağlar, production'da spesifik domain ekle!
            allow_credentials=True,
            allow_methods=["*"],  # GET, POST, PUT, DELETE gibi tüm metodları kabul et
            allow_headers=["*"],  # Tüm başlıkları kabul et
        )
    - ```python
        import os
        DEBUG = os.getenv("DEBUG", "False") == "True"
    
    - FastAPI, hata mesajlarını yönetmek için özel bir exception_handler tanımlamana izin verir.Eklemek için:
        ```python
        from fastapi.responses import JSONResponse
        @app.exception_handler(Exception)
        async def general_exception_handler(request, exc):
            return JSONResponse(
                status_code=500,
                content={"message": f"Beklenmeyen bir hata oluştu: {str(exc)}"},
            )

### models.py we are gonna make table inside it.
We define tables here. Examples are:
- ```python
    from database import Base
    from sqlalchemy import Column, Integer, String, Boolean, ForeignKey


    class User(Base):
        __tablename__ = "users"
        id = Column(Integer, primary_key = True, index=True) 
        email = Column(String, unique=True)
        username = Column(String,unique=True)
        first_name = Column(String)
        last_name = Column(String)
        hashed_password = Column(String)
        is_active = Column(Boolean ,default=True)
        role = Column(String)
        phone_number = Column(Integer, nullable=True)

### database.py we are gonna make database setting inside the project.
This file is responsible for connecting to the database and setting up the SQLAlchemy ORM for projects.
- SQLALCHEMY_DATABASE_URL = "postgresql://username:password@ip:port/dbname"
- engine = create_engine(SQLALCHEMY_DATABASE_URL)  
    - create_engine used for connection between SQLALCHEMY and database.
    - Lazy connection which means connection is not created immediately, instead, it's established when needed.
- SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind = engine)
    - This creates a session factory, allowing us to interact with database.
    - autocommit = False means transactions are not commited automatically(you need to manually commit(.commit()))
    - autoflush = False means Changes are not automatically flushed to database before queries.
    - bind = engine Associative this session with our database engine.
    - This function provides a database session in a dependency injection format. 
    ```python 
        from database import SessionLocal

        def get_db():
            db = SessionLocal()
            try:
                yield db  # Generator to provide a session
            finally:
                db.close()  # Always close the session after use

- declaring the Base Model Base = declarative_base()
    - declarative_base() is a base-class that all models inherit from.
    - This is needed because SQLAlchemy uses ORM models to map Python classes to database tables.
    - More secure and Professional
    ```python
        import os
        import logging
        from dotenv import load_dotenv
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        from sqlalchemy.ext.declarative import declarative_base

        # Load environment variables
        load_dotenv()

        # Get database URL from .env file
        SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

        # Create engine with connection pooling
        engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_size=20, max_overflow=0)

        # Create session factory
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

        # Base class for models
        Base = declarative_base()

        # Enable SQL query logging (for debugging)
        logging.basicConfig()
        logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


### What is Apirouters and why we use it?
APIRouter is a modular way to define and organize routes in FastAPI. Instead of defining all endpoints inside main.py, we use APIRouter to split our API into smaller, reusable modules.

### How to get path parameters and query parameters
- Path parameters are part of the URL path and are used to identify a specific resource.
    ```python
        from fastapi import FastAPI

        app = FastAPI()

        @app.get("/users/{user_id}")
        def get_user(user_id: int):
            return {"user_id": user_id}
- Path parementer validation example
    ```python
        from fastapi import Path

        @app.get("/users/{user_id}")
        def get_user(user_id: int = Path(..., title="User ID", ge=1, le=1000)):
            return {"user_id": user_id}


- Query parameters are sent after the  in the URL and are optional by default. GET /search?q=fastapi

    ```python
        @app.get("/search")
        def search_items(q: str):
            return {"query": q}

If a query parameter is optional, you can set a default value.
- ```python
        @app.get("/products")
        def get_products(limit: int = 10, page: int = 1):
            return {"limit": limit, "page": page}

Query parameters validation.
- ```python
    from fastapi import Query

    @app.get("/search")
    def search(q: str = Query(..., min_length=3, max_length=20, title="Search Query")):
        return {"query": q}

### How to define Foreignkey and make operations based on it.
- we define different ways worked one is in the models.py file but below code more enhancement way to relationships
ForeignKey("users.id") → user_id column in todos table references id in users table.
relationship("User", back_populates="todos") → Defines the relationship between User and Todo (one-to-many).

-    ```python
        from sqlalchemy import Column, Integer, String, ForeignKey
        from sqlalchemy.orm import relationship
        from database import Base

        class User(Base):
            __tablename__ = "users"

            id = Column(Integer, primary_key=True, index=True)
            username = Column(String, unique=True, index=True)
            password = Column(String)

            # Relationship to Todos
            todos = relationship("Todo", back_populates="owner")


        class Todo(Base):
            __tablename__ = "todos"

            id = Column(Integer, primary_key=True, index=True)
            title = Column(String, index=True)
            description = Column(String)
            user_id = Column(Integer, ForeignKey("users.id"))

            # Relationship to User
            owner = relationship("User", back_populates="todos")

- By default, SQLAlchemy does not automatically delete related records.
To enable cascade delete, modify the User model:
- ```python
    class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

    todos = relationship("Todo", back_populates="owner", cascade="all, delete")

- ```python
    @app.delete("/users/{user_id}")
    def delete_user(user_id: int, db: Session = Depends(get_db)):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return {"error": "User not found"}
        
        db.delete(user)
        db.commit()
        return {"message": "User deleted successfully"}

### How to make Many2Many Relations and operations
- A Many-to-Many (M2M) relationship occurs when multiple records in one table relate to multiple records in another table. In SQLAlchemy, we achieve this using an association table.
Let's consider:
Users can have multiple Roles.
Roles can belong to multiple Users.
- ```python
    from sqlalchemy import Column, ForeignKey, Integer, Table
    from sqlalchemy.orm import relationship
    from database import Base

    # Many-to-Many Association Table
    user_role_association = Table(
        "user_role",
        Base.metadata,
        Column("user_id", Integer, ForeignKey("users.id")),
        Column("role_id", Integer, ForeignKey("roles.id"))
    )

- define user and role models
    - ```python
        class User(Base):
            __tablename__ = "users"

            id = Column(Integer, primary_key=True, index=True)
            username = Column(String, unique=True, index=True)

            roles = relationship("Role", secondary=user_role_association, back_populates="users")


        class Role(Base):
            __tablename__ = "roles"

            id = Column(Integer, primary_key=True, index=True)
            name = Column(String, unique=True)

            users = relationship("User", secondary=user_role_association, back_populates="roles")

- How about views for add role to user
    - ```python
       @app.post("/users/{user_id}/roles/{role_id}")
        def add_role_to_user(user_id: int, role_id: int, db: Session = Depends(get_db)):
            user = db.query(User).filter(User.id == user_id).first()
            role = db.query(Role).filter(Role.id == role_id).first()

            if not user or not role:
                return {"error": "User or Role not found"}

            user.roles.append(role)
            db.commit()
            return {"message": f"Role {role.name} added to User {user.username}"}

- Get Roles for user
    - ```python
       @app.get("/users/{user_id}/roles")
        def get_user_roles(user_id: int, db: Session = Depends(get_db)):
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return {"error": "User not found"}
            return {"username": user.username, "roles": [role.name for role in user.roles]}

- Removes a role from user
 - ```python
    @app.delete("/users/{user_id}/roles/{role_id}")
    def remove_role_from_user(user_id: int, role_id: int, db: Session = Depends(get_db)):
        user = db.query(User).filter(User.id == user_id).first()
        role = db.query(Role).filter(Role.id == role_id).first()

        if not user or not role:
            return {"error": "User or Role not found"}

        user.roles.remove(role)
        db.commit()
        return {"message": f"Role {role.name} removed from User {user.username}"}

- Get users with specific role
 - ```python
    @app.get("/roles/{role_id}/users")
    def get_users_by_role(role_id: int, db: Session = Depends(get_db)):
        role = db.query(Role).filter(Role.id == role_id).first()
        if not role:
            return {"error": "Role not found"}
        return {"role": role.name, "users": [user.username for user in role.users]}

### How to make Authenticate and Authorization in FastApi.
In FastAPI, Authentication verifies who the user is, while Authorization checks what they can do. We commonly use JWT (JSON Web Token) for authentication.
- install dependencies
    fastapi[all] → Installs required dependencies.
    passlib[bcrypt] → Hashes passwords securely.
    pyjwt → Generates & verifies JWT tokens.

    ```bash
        pip install fastapi[all] passlib bcrypt pyjwt

- Define user model 
    - ```python
        from sqlalchemy import Column, Integer, String
        from database import Base

        class User(Base):
            __tablename__ = "users"

            id = Column(Integer, primary_key=True, index=True)
            username = Column(String, unique=True, index=True)
            email = Column(String, unique=True, index=True)
            hashed_password = Column(String)

- setup password hashing
    - ```python
        from passlib.context import CryptContext
        from database import SessionLocal

        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

        def get_password_hash(password: str) -> str:
            return pwd_context.hash(password)

        def verify_password(plain_password: str, hashed_password: str) -> bool:
            return pwd_context.verify(plain_password, hashed_password)

        def get_db():
            db = SessionLocal()
            try:
                yield db
            finally:
                db.close()

- JWT token Generation
 - ```python
    from datetime import datetime, timedelta
    from jose import JWTError, jwt

    SECRET_KEY = "mysecretkey"
    ALGORITHM = "HS256"
    def create_access_token(username:str,role:str, user_id:int, expires_delta:timedelta ):
        encode ={
            'sub':username, 'id':user_id, "role":role
        }
        expires = datetime.now(timezone.utc) + expires_delta
        encode.update({'exp':expires})
        return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    @router.post('/auth/token')
    async def login_for_access_token(form_data:Annotated[OAuth2PasswordRequestForm, Depends()],
                                    db:db_dependency):

        user = authenticate_user(form_data.username,form_data.password, db)
        
        if not user:
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
        
        token = create_access_token(user.username,user.role, user.id,timedelta(minutes=20) )
        return {'access_token': token, 'token_type':'Bearer'}
    from fastapi.security import OAuth2PasswordBearer
    from fastapi import Security

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

    def get_current_user(token: str = Security(oauth2_scheme), db: Session = Depends(get_db)):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if not username:
                raise HTTPException(status_code=401, detail="Invalid token")
            user = db.query(User).filter(User.username == username).first()
            if not user:
                raise HTTPException(status_code=401, detail="User not found")
            return user
        except JWTError:
            raise HTTPException(status_code=401, detail="Token expired or invalid")


### How to make alembic data migration What is order it?
- pip install alembic
-  FastAPI project directory
    - alembic init alembic   #  which create the alembic name of the alembic
        -   /alembic
                /versions    # Stores migration files
                env.py       # Alembic configuration
            alembic.ini      # Main config file
- configure alembic with <b> alembic.ini </b>
    - ```ini
        sqlalchemy.url = postgresql://username:password@localhost:5432/dbname

- configure alembic/env.py
    you can edit fileConfig get rid of the if condition, and you need to setup target_metadata
    - ```python
        # Load config
        config = context.config
        fileConfig(config.config_file_name)
        target_metadata = Base.metadata

- What is Base.metadata?
    In SQLAlchemy, Base.metadata contains metadata information about all the tables defined using Base.For example, in your FastAPI project, you define a Base class in models.py:
    - ```python
        from database import Base
        from sqlalchemy import Column, Integer, String, Boolean, ForeignKey


        class User(Base):
            __tablename__ = "users"
            id = Column(Integer, primary_key = True, index=True) 
            email = Column(String, unique=True)
            username = Column(String,unique=True)
            first_name = Column(String)
            last_name = Column(String)
            hashed_password = Column(String)
            is_active = Column(Boolean ,default=True)
            role = Column(String)
            phone_number = Column(Integer, nullable=True)
            phone_number2 = Column(Integer, nullable=True)

    Now, every model that inherits from Base (e.g., Todos, User) is automatically registered in Base.metadata.

-  Why Use target_metadata = Base.metadata?
    In alembic/env.py, we set:
    - ```python
        target_metadata = Base.metadata

    This tells Alembic:

    Look at Base.metadata to find all models (User, Todos, etc.). Compare these models with the current database schema. Generate migrations automatically based on differences. If you don't set target_metadata, Alembic won't know which tables to track, and --autogenerate won't work.

- Create first migration
    - ```bash
        alembic revision --autogenerate -m "Initial migration"

- Apply migration to Database
    - ```bash
        alembic upgrade head or alembic upgrade <revision_id> which is inside to migration file 


- Command	Description
    - alembic init alembic ==>	Initialize Alembic
    - alembic revision --autogenerate -m "message" ===>	Create a new migration
    - alembic upgrade head ===>	Apply all migrations
    - alembic downgrade -1 ===>	Rollback last migration
    - alembic history	===> Show migration history



(Below is the getting soon .....)
### How to make test in the FastApi

### Deploying FastAPI Applications

### How to make fullstack app with FastApi




