


from pickletools import OpcodeInfo
from unittest import result
from fastapi import APIRouter, Depends, HTTPException, status
from app.database import get_db
from sqlalchemy.orm import Session
from app import models
from app.skema import Event, EventBase, EventOut
from typing import List, Optional
from sqlalchemy import DateTime, outerjoin, select, update, delete, insert, and_


from .. skema import TokenData, User
from .. import oauth2
from datetime import datetime



router  = APIRouter(prefix="/info", tags=["Info", "Events"])

@router.get("/events", response_model=List[EventOut])
def get_events(*, db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = "", user: TokenData = Depends(oauth2.try_token)):
    if not user:
        result = db.execute(select(models.Event).limit(limit).offset(skip).where(models.Event.name.contains(search)))
        events = result.scalars().all()  # It should be scalars().all(), not scalars.all()
        if not events:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No events found.")
        return events
    else:
        smt = select(models.Event, models.save).join(
        models.save, and_(models.save.c.event_id == models.Event.id,models.save.c.user_id == user.id),isouter=True )
     
        
        result = db.execute(smt)
        events = []
        for event, save, id in result:
              # 'event' is an instance of 'models.Event', 'save' could be 'models.save' or None
            events.append(EventOut(id = event.id, track = event.track, name = event.name, event_start=event.event_start, description=event.description, time = event.time, img = event.img, link = event.link, is_saved = True if id else False))  

        return events



"""@router.get("/events/user")
def test(db: Session = Depends(get_db), user: User = Depends(oauth2.get_current_user)):
        smt = select(models.Event, models.save).join(
        models.save, and_(models.save.c.event_id == models.Event.id,models.save.c.user_id == user.id),isouter=True )
     
        
        result = db.execute(smt)
        events = []
        for event, save, id in result:
              # 'event' is an instance of 'models.Event', 'save' could be 'models.save' or None
            events.append(EventOut(id = event.id, track = event.track, name = event.name, date = event.date, description=event.description, time = event.time, img = event.img, link = event.link, is_saved = True if id else False))  # Assuming you still want to collect 'models.Event' instances

        if not events:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No events found.")

        return events"""


   

@router.get("/events/{id}", response_model=EventOut)
def get_event(*, db: Session = Depends(get_db), id: int):
    result = db.execute(select(models.Event).where(models.Event.id == id))
    event = result.scalars().first()
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return event



@router.post("/events",status_code=status.HTTP_201_CREATED, response_model= Event)
def create_event(*, db: Session = Depends(get_db), event: EventBase):
   
    if event.event_start:
        event_time = datetime(event.event_start.year, event.event_start.month, event.event_start.day, event.event_start.hour, event.event_start.minute)
    else:
        event_time = None
    result = db.execute(insert(models.Event).returning(models.Event).values(track = event.track, name=event.name, event_start = event_time, description = event.description, time=event.time, img = event.img, link = event.link))
    db.commit()
    created = result.scalars().first()
    if not created:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return created


@router.put("/events/{id}", response_model=Event, status_code=status.HTTP_201_CREATED)
def update_event(*, db: Session = Depends(get_db), id: int, event: EventBase):
    result = db.execute( update(models.Event).returning(models.Event).where(models.Event.id == id).values(track = event.track, name = event.name, date = event.date, description = event.description, time = event.time, img = event.img, link = event.link))
    event = result.scalars().first()
    if not event: 
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) 
    return event

@router.delete("/events/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(*, db: Session = Depends(get_db), id: int):
    res = db.execute(delete(models.Event).returning(models.Event).where(models.Event.id == id))
    db.commit()
    deleted = res.scalars().first()
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    