
from fastapi import Depends, HTTPException,status
from sqlalchemy import select
from sqlalchemy.orm import Session
from jose import JWSError, JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
from app import skema
from app.database import get_db
from . import models
from.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# secret key 

#alorithm 

#eperation  time 


SECRET_KEY = "1f19d4458acd56220a5a3c18b39de46fa7bef5556d5d36724b8be6e3acf082c3"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_token(data: dict):
    expires_Delta = timedelta(minutes=settings.access_token_expire_minutes)
    to_encode = data.copy()
    if expires_Delta:
        expire = datetime.now(timezone.utc) + expires_Delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return skema.Token(access_token=encoded_jwt,token_type="Bearer")

def verify_token(token: str, credintialsExeption):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    
        id = payload.get("user_id")
       
        if id is None :
            raise credintialsExeption
        token_data = skema.TokenData(id=id)
    except :
        raise credintialsExeption
    return token_data


def get_current_user(token:str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exeption = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate headers", headers={"www-Authenticate": "Bearer"})
     
    tk = verify_token(token, credentials_exeption)
    
    request = db.execute(select(models.User).where(models.User.id == tk.id))
    user = request.scalars().first()
    return user 
 
# optinal login 
ns = OAuth2PasswordBearer(tokenUrl="login", auto_error=False)   
def try_token(token: str = Depends(ns)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    
        id = payload.get("user_id")
       
        
       
        if id == None:
            token_data = skema.TokenData()
        else:
            token_data = skema.TokenData(id=id)
        
    except:
       token_data = skema.TokenData()
    return token_data

    