
from .database import Base
from sqlalchemy import String, ARRAY
from sqlalchemy.orm import mapped_column, Mapped
from typing import List



class Event(Base):
    __tablename__ = "event"
    
    
    id : Mapped[int] = mapped_column(primary_key=True, nullable=False)
    track: Mapped[str] = mapped_column(primary_key=False, nullable=False)
    name: Mapped[str] = mapped_column(primary_key=False, nullable=False)
    date: Mapped[str] = mapped_column(primary_key=False,nullable=False)
    description: Mapped[str] = mapped_column(primary_key=False,nullable=True)
    time: Mapped[List[str]] = mapped_column(ARRAY(String), nullable=True)
    img: Mapped[str] = mapped_column(primary_key=False,nullable=True)
    link: Mapped[str] = mapped_column(primary_key=False, nullable=True)



