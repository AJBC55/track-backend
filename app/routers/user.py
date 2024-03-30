
from os import error
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models
from app.skema import TokenData, User, UserBase, UserInfo
from app.database import get_db
from sqlalchemy import delete, select, insert, update
from typing import List
from .. import utils 
from .. import oauth2





router = APIRouter(tags=["User"])



@router.get("/user", response_model= List[UserInfo])
def get_users(*,db: Session = Depends(get_db), admin: User = Depends(oauth2.get_current_user)): 
    if not admin.is_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Admin privaleges required")
    result = db.execute(select(models.User).limit(20))
    users = result.scalars().fetchall()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return users 



@router.get("/user/{id}", response_model= UserInfo)
def get_user(*, db: Session = Depends(get_db), id: int): 
    result = db.execute(select(models.User).where(models.User.id == id))
    user = result.scalars().first()
    if not user: 
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED)
    return user 
    
@router.post("/user", status_code=status.HTTP_201_CREATED)
def create_user(*, db: Session = Depends(get_db), user_data: UserBase):
    # Hash the user's password
    hashed_password = utils.phash(user_data.password)
    # Prepare the insert statement
    try:
    
        result = db.execute(insert(models.User).values(
        email=user_data.email,
        password=hashed_password, 
        name_first=user_data.name_first,
        name_last=user_data.name_last, is_admin = user_data.is_admin).returning(models.User))
    except:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
        
    
    user_response = result.scalars().first()
        
    db.commit()
    

    
    return user_response


@router.put("/user/{id}", response_model=User, status_code=status.HTTP_201_CREATED)
def update_user(*, db: Session = Depends(get_db), user: UserBase, id: int, usr: User = Depends(oauth2.get_current_user)):
    if not usr.is_admin or usr.id != id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user_dict = user.model_dump(exclude_none=True)
    result = db.execute(update(models.User).where(models.User.id == id).values(**user_dict).returning(models.User))
    updated = result.scalars().first()
    db.commit()
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return updated


@router.delete("/user/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(*, db: Session = Depends(get_db), id: int, usr: User = Depends(oauth2.get_current_user)):
    if not usr.is_admin or usr.id != id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    result = db.execute(delete(models.User).returning(models.User).where(models.User.id == id))
    deleted = result.scalar()
    db.commit()
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    