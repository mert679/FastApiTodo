##This below code is for sqlite3 compatibility
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base


# SQLALCHEMY_DATABASE_URL = "sqlite:///./todosapp.db"
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args ={'check_same_thread':False})
# SessionLocal = sessionmaker(autocommit=False,autoflush = False, bind = engine)

# Base = declarative_base()
#-----------------------------------------------------------------
## Below code for postgresql compatibility
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:mert1453@localhost:5432/Fast"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False,autoflush = False, bind = engine)

Base = declarative_base()