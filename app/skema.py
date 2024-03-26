import datetime
from pydantic import BaseModel
from typing import List, Optional

from sqlalchemy import DateTime






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
    track: Optional[str] = None
    title: str
    date: Optional[str] = None
    body: Optional[str] = None 
    
# sub pydantic model of news event:
class News(NewsBase):
    id : int
    
    
    class from_atributes:
        orm_mode = True
    
    
#pydantic model for a user
class UserBase(BaseModel):
    email: str
    password:str
    name_first: Optional[str] = None
    name_last: Optional[str] = None

# pydantic model for user 
class User(UserBase):
    id: int
   
    
    class from_atributes:
        orm_mode = True
        
        
        
class UserInfo(BaseModel):
    id: int
    email:str
    name_first: Optional[str] = None
    name_last: Optional[str] = None
    created_at: datetime.datetime
    
    class Config:
        from_attributes  = True 
    
    
    
class UserLogin(BaseModel):
    email: str
    password: str 
    
    
class Token(BaseModel):
    access_token: str 
    token_type: str 
    
    
    
class TokenData(BaseModel):
    id: Optional[int] = None
    
    
#pydanic models for save result


class EventOut(BaseModel):
    id: int
    track: str
    name : str
    date: str
    description: Optional[str] = None 
    time: Optional[List[str]] = None
    img: Optional[str] = None
    link: Optional[str] = None 
    is_saved: Optional[bool] = False