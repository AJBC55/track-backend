from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.database import get_db
from app.skema import Token
from app import models
from sqlalchemy import select
from sqlalchemy.orm import Session
from app import utils
from app import oauth2




router = APIRouter(prefix="/login", tags=["Authentication"])




@router.post("", response_model=Token)
def login(*, db: Session = Depends(get_db), login : OAuth2PasswordRequestForm = Depends()):
    password = login.password
    email = login.username 
    result = db.execute(select(models.User).where(models.User.email == email))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="INVALID CREDENTIALS")
    if not utils.verify(login.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="INVALID CREDENTIALS")
    acces_token = oauth2.create_token(data={"user_id": user.id})
    return acces_token
    