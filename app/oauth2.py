from fastapi import Depends, HTTPException,status
from sqlalchemy import select
from sqlalchemy.orm import Session
from jose import JWSError, JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
from app import skema
from app.database import get_db
from . import models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# secret key 

#alorithm 

#eperation  time 


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_token(data: dict):
    expires_Delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = data.copy()
    if expires_Delta:
        expire = datetime.now(timezone.utc) + expires_Delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
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
    
    