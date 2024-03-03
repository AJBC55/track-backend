

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update

from app.database import get_db
from app import models
from app.skema import NewsBase




router = APIRouter(prefix="/info")



# get all news

@router.get("/news")
def get_news(db: Session = Depends(get_db)):
    result = db.execute(select(models.News))
    events = result.scalars().all()
    if not events:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
# get news by id 

@router.get("/news/{id}")
def get_news_id(*, db: Session = Depends(get_db), id: int):
    # create a db query
    result = db.execute(select(models.News).where(models.News.id == id))
    # parse the query
    event = result.scalars().first()
    
    if not event: 
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    
@router.post("/news")
def create_news(*, db: Session = Depends(get_db), news : NewsBase):
    result = db.execute(insert(models.News).values(track = news.track, title = news.title, date = news.date, body = news.body).returning(models.News))
    event = result.scalars().first()
    if not event: 
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return event


@router.post("/event/{id}")
def update_news(*, db: Session = Depends(get_db), news: NewsBase): 
    result = db.execute(update())
    
    