



from fastapi import APIRouter, Depends, HTTPException, status
from app.database import get_db
from sqlalchemy.orm import Session
from app import models
from app.skema import Event, EventBase, EventOut
from typing import List, Optional
from sqlalchemy import DateTime, outerjoin, select, update, delete, insert, and_
from fastapi.responses import Response


from .. skema import TokenData, User
from .. import oauth2
from datetime import datetime



router  = APIRouter(prefix="/events", tags=["Events"])

@router.get("", response_model=List[EventOut])
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
            events.append(EventOut(id = event.id, track = event.track, name = event.name, event_start=event.event_start, description=event.description, time = event.time, img_link = event.img_link, link = event.link, is_saved = True if id else False))  

        return events


@router.get("/{id}", response_model=EventOut)
def get_event(*, db: Session = Depends(get_db), id: int):
    result = db.execute(select(models.Event).where(models.Event.id == id))
    event = result.scalars().first()
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return event

@router.get("/events/img/{id}")
def get_event_img(*, db: Session = Depends(get_db), id: int):
    result = db.execute(select(models.Event.event_img).where(models.Event.id == id))
    img = result.scalar_one_or_none()
    if not img:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return Response(img, media_type="image/png")








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