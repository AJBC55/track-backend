from fastapi import APIRouter, Depends, HTTPException, status
from app.database import get_db
from sqlalchemy.orm import Session
from app import models
from app.skema import Event, EventBase, EventOut
from typing import List, Optional
from sqlalchemy import DateTime, outerjoin, select, update, delete, insert, and_
from datetime import datetime
from ..skema import User
from .. import oauth2



router = APIRouter(tags=["Admin"])



@router.post("/events",status_code=status.HTTP_201_CREATED, response_model= Event)
def create_event(*, db: Session = Depends(get_db), event: EventBase, user: User = Depends(oauth2.get_current_user)):
    
    if not user.is_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "Admin privalages required")
   
    if event.event_start:
        event_time = datetime(event.event_start.year, event.event_start.month, event.event_start.day, event.event_start.hour, event.event_start.minute)
    else:
        event_time = None
    result = db.execute(insert(models.Event).returning(models.Event).values(track = event.track, name=event.name, event_start = event_time, event_end = event.event_end, description = event.description, time=event.time, img = event.img, link = event.link))
    db.commit()
    created = result.scalars().first()
    if not created:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return created



@router.put("/events/{id}", response_model=Event, status_code=status.HTTP_201_CREATED)
def update_event(*, db: Session = Depends(get_db), id: int, event: EventBase,  user: User = Depends(oauth2.get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "Admin privalages required")
    result = db.execute( update(models.Event).returning(models.Event).where(models.Event.id == id).values(track = event.track, name = event.name, event_start = event.event_start, event_end = event.event_end, description = event.description, time = event.time, img = event.img, link = event.link))
    event = result.scalars().first()
    if not event: 
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) 
    return event



@router.delete("/events/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(*, db: Session = Depends(get_db), id: int,  user: User = Depends(oauth2.get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "Admin privalages required")
    res = db.execute(delete(models.Event).returning(models.Event).where(models.Event.id == id))
    db.commit()
    deleted = res.scalars().first()
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)