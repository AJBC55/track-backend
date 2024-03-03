
from .database import Base
from sqlalchemy import FallbackAsyncAdaptedQueuePool, String, ARRAY, DateTime, text
from sqlalchemy.orm import mapped_column, Mapped
from typing import List



class Event(Base):
    __tablename__ = "event"
    
    
    id : Mapped[int] = mapped_column(primary_key=True, nullable=False)
    track: Mapped[str] = mapped_column(primary_key=False, nullable=True)
    name: Mapped[str] = mapped_column(primary_key=False, nullable=False)
    date: Mapped[str] = mapped_column(primary_key=False,nullable=False)
    description: Mapped[str] = mapped_column(primary_key=False,nullable=True)
    time: Mapped[List[str]] = mapped_column(ARRAY(String), nullable=True)
    img: Mapped[str] = mapped_column(primary_key=False,nullable=True)
    link: Mapped[str] = mapped_column(primary_key=False, nullable=True)
    created_at = Mapped[str] = mapped_column(DateTime(timezone=True),server_default=text('now()'))
    
    
class News(Base):
    __tablename__ = "news"
    
    
    id : Mapped[int] = mapped_column(primary_key=True, nullable=False)
    track: Mapped[str] = mapped_column(primary_key=False, nullable=True)
    title: Mapped[str] = mapped_column(primary_key=False, nullable=False)
    date: Mapped[str] = mapped_column(primary_key=False, nullable=True)
    body: Mapped[str] = mapped_column(primary_key=False, nullable=True)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=text('now()'))
    
class User(Base): 
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    name_first: Mapped[str] = mapped_column(primary_key=False, nullable=True)
    name_last: Mapped[str] = mapped_column(primary_key=False,nullable=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(primary_key=False)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True),server_default=text('now()'))
    
    



