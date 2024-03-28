from fastapi import APIRouter, Depends, HTTPException, status
from app.database import get_db
from sqlalchemy.orm import Session
from app import models
from app.skema import Event, EventBase, EventOut
from typing import List, Optional
from sqlalchemy import outerjoin, select, update, delete, insert, and_
from .. skema import TokenData, User
from .. import oauth2


router = APIRouter(prefix="/info/events", tags=["Events", "Save"])



@router.get("/save",response_model=List[Event])
def get_saved_events(*, db: Session = Depends(get_db), user: User = Depends(oauth2.get_current_user), limit: int = 10):
    result = db.execute(select(models.Event).join(models.save).where(models.save.c.user_id == user.id).limit(limit))
    saved_events = result.scalars().all()
    if not saved_events:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return saved_events




@router.post("/save/{id}")
def save_event(*, db:Session = Depends(get_db), user: User = Depends(oauth2.get_current_user),id:int):
    event_result = db.execute(select(models.Event).where(models.Event.id == id))
    event = event_result.scalars().first()
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Event does not exist")
    found = db.execute(select(models.save).where(models.save.c.user_id == user.id, models.save.c.event_id == id))
    found_like = found.scalars().first()
    if found_like:
        db.execute(delete(models.save).where(models.save.c.user_id == user.id, models.save.c.event_id == id))
        db.commit()
        return {id : "unsaved"}
    else:  
        result = db.execute(insert(models.save).values(user_id = user.id, event_id = id).returning(models.save))
        db.commit()
        relation = result.scalars().all()
        if not relation :
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Could Not Save")
        return {id: "saved"}
    