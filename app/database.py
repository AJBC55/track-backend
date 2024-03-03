from sqlalchemy import create_engine
from sqlalchemy.orm import  sessionmaker, DeclarativeBase

sqlalchemy_database_url = "postgresql://postgres:Fizzy1335!@localhost/track"


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


