from pydantic import BaseModel
from typing import List, Optional






# creates the base for event base, it is a pydantic model, it is what is accepted by the api
class EventBase(BaseModel):
    track: str
    name : str
    date: str
    description: Optional[str] = None 
    time: Optional[List[str]] = None
    img: Optional[str] = None
    link: Optional[str] = None 
    
    
    
# this is the pydantic model that will be returned in the api  
class Event(EventBase):
    id: int
    
    
    class from_atributes:
        orm_mode = True
    

# pydantic model for a news event
class NewsBase(BaseModel):
    track: Optional[str]
    title: str
    date: Optional[str]
    body: Optional[str]
    
# sub pydantic model of news event:
class News(NewsBase):
    id : int
    
    
    class from_atributes:
        orm_mode = True
    
    
#pydantic model for a user
class UserBase(BaseModel):
    email: str
    password:str
    name_first: Optional[str]
    name_last: Optional[str]

# pydantic model for user 
class User(UserBase):
    id: int
   
    
    class from_atributes:
        orm_mode = True