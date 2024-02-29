from pydantic import BaseModel
from typing import List, Optional


class EventBase(BaseModel):
    track: str
    name : str
    date: str
    description: Optional[str] = None 
    time: Optional[List[str]] = None
    img: Optional[str] = None
    link: Optional[str] = None 
    
    
    
    
class Event(EventBase):
    id: int
    
    
    class from_atributes:
        orm_mode = True
    
    