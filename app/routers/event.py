
from fastapi import APIRouter, Depends, HTTPException, status
from app.database import get_db
from sqlalchemy.orm import Session
from app import models
from app.skema import Event, EventBase
from typing import List
from sqlalchemy import select, update, delete, insert




router  = APIRouter(prefix="/info")

@router.get("/event", response_model=List[Event])
def get_events(db: Session = Depends(get_db)):
    result = db.execute(select(models.Event))
    events = result.scalars().all()  # It should be scalars().all(), not scalars.all()
    if not events:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No events found.")
    return events


@router.get("/event/{id}", response_model=Event)
def get_event(*, db: Session = Depends(get_db), id: int):
    result = db.execute(select(models.Event).where(models.Event.id == id))
    event = result.scalars().all()
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return event



@router.post("/event",status_code=status.HTTP_201_CREATED, response_model= Event)
def create_event(*, db: Session = Depends(get_db), event: EventBase):
    result = db.execute(insert(models.Event).returning(models.Event).values(track = event.track, name=event.name, date=event.date, description = event.description, time=event.time, img = event.img, link = event.link))
    db.commit()
    created = result.scalars().all()
    if not created:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return created


@router.put("/events/{id}", response_model=Event, status_code=status.HTTP_201_CREATED)
def update_event(*, db: Session = Depends(get_db), id: int, event: EventBase):
    result = db.execute( update(models.Event).where(models.Event.id == id).values(track = event.track, name = event.name, date = event.date, description = event.description, time = event.time, img = event.img, link = event.link))
    event = result.scalars().all()
    if not event: 
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) 
    return event

@router.delete("/events/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(*, db: Session = Depends(get_db), id: int):
    db.execute(delete(models.Event).where(models.Event.id == id))
    db.commit()
    