import contextlib
from sqlalchemy.ext.asyncio import create_async_engine, AsyncAttrs, async_sessionmaker
from sqlalchemy.orm import   DeclarativeBase
from .config import settings


#//user:password@hostname/database_name

sqlalchemy_database_url = f"postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"


engine = create_async_engine(sqlalchemy_database_url)


SessionLocal = async_sessionmaker(expire_on_commit=False,autoflush=False,bind=engine)

class Base( AsyncAttrs, DeclarativeBase):
    pass




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


