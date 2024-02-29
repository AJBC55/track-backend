from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

sqlalchemy_database_url = "postgresql://postgres:Fizzy1335!@localhost/track"


engine = create_engine(sqlalchemy_database_url)


SessionLocal = sessionmaker(expire_on_commit=False,autoflush=False,bind=engine)

Base = declarative_base()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


