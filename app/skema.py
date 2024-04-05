import datetime
from pydantic import BaseModel, EmailStr
from typing import List, Optional



class DateTime(BaseModel):
    year: int
    month: int
    day: int
    hour: int
    minute: int
    




# creates the base for event base, it is a pydantic model, it is what is accepted by the api
class EventBase(BaseModel):
    track: str
    name : str
    event_start: Optional[DateTime] = None
    event_end: Optional[DateTime] = None
    description: Optional[str] = None 
    time: Optional[List[str]] = None
    img_link : Optional[str] = None
    ticket_link: Optional[str] = None 
    
    
    
# this is the pydantic model that will be returned in the api  
class Event(EventBase):
    id: int
    event_start: Optional[datetime.datetime]
    
    
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
    username: str
    email: EmailStr
    password:str
    phone_number: Optional[str] = None
    name_first: Optional[str] = None
    name_last: Optional[str] = None
    is_admin: Optional[bool] = False


# pydantic model for user 
class User(UserBase):
    id: int
    is_admin: bool 
    
   
    
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
    description: Optional[str] = None 
    time: Optional[List[str]] = None
    img_link: Optional[str] = None
    ticket_link: Optional[str] = None
    event_start: Optional[datetime.datetime]
    is_saved: Optional[bool] = False