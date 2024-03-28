
from .database import Base
from sqlalchemy import FallbackAsyncAdaptedQueuePool, String, ARRAY, DateTime, text, Table, Column, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import List


save = Table(
    "save",
    Base.metadata,
    Column("event_id", ForeignKey("event.id"), primary_key=True),
    Column("user_id", ForeignKey("user.id"),primary_key=True))


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
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True),server_default=text('now()'))
    
    
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
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(primary_key=False)
    name_first: Mapped[str] = mapped_column(primary_key=False, nullable=True)
    name_last: Mapped[str] = mapped_column(primary_key=False,nullable=True)
    is_admin: Mapped[bool] = mapped_column(primary_key=False, server_default=text("false"), nullable=True)
    saved_events: Mapped[List[Event]] = relationship( secondary=save,cascade="all, delete")
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True),server_default=text('now()'))

    




    