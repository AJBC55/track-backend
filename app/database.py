from sqlalchemy import create_engine
from sqlalchemy.orm import  sessionmaker, DeclarativeBase
from .config import settings



#//user:password@hostname/database_name

sqlalchemy_database_url = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}"


engine = create_engine(sqlalchemy_database_url)


SessionLocal = sessionmaker(expire_on_commit=False,autoflush=False,bind=engine)

class Base(DeclarativeBase):
    pass




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


