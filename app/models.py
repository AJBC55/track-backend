
from .database import Base
from sqlalchemy import  String, ARRAY, DateTime, text, Table, Column, ForeignKey, LargeBinary
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import List
from datetime import datetime



save = Table(
    "save",
    Base.metadata,
    Column("event_id", ForeignKey("event.id", ondelete="CASCADE"), primary_key=True),
    Column("user_id", ForeignKey("user.id", ondelete="CASCADE"),primary_key=True))


class Event(Base):
    __tablename__ = "event"
    
    
    id : Mapped[int] = mapped_column(primary_key=True, nullable=False)
    track: Mapped[str] = mapped_column(primary_key=False, nullable=True)
    name: Mapped[str] = mapped_column(primary_key=False, nullable=False)
    event_start: Mapped[str] = mapped_column(DateTime, nullable=True)
    event_end: Mapped[str] = mapped_column(DateTime, nullable=True)
    time: Mapped[List[str]] = mapped_column(ARRAY(String), nullable=True)
    description: Mapped[str] = mapped_column(primary_key=False,nullable=True)
    time: Mapped[List[str]] = mapped_column(ARRAY(String), nullable=True)
    img_link: Mapped[str] = mapped_column(primary_key=False,nullable=True)
    link: Mapped[str] = mapped_column(primary_key=False, nullable=True)
    event_img: Mapped[bytes] = mapped_column(LargeBinary(), nullable=True)
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
    username: Mapped[str] = mapped_column(primary_key=True, unique=True)
    password: Mapped[str] = mapped_column(primary_key=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    phone_number: Mapped[str] = mapped_column(nullable=True)
    name_first: Mapped[str] = mapped_column(primary_key=False, nullable=True)
    name_last: Mapped[str] = mapped_column(primary_key=False,nullable=True)
    is_admin: Mapped[bool] = mapped_column(primary_key=False, server_default=text("false"), nullable=True,)
    saved_events: Mapped[List[Event]] = relationship( secondary=save)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True),server_default=text('now()'))

    




    