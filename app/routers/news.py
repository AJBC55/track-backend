

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import delete, select, insert, update

from app.database import get_db
from app import models
from app.skema import NewsBase, News




router = APIRouter(prefix="/info")



# get all news

@router.get("/news", response_model= News)
def get_news(db: Session = Depends(get_db)):
    result = db.execute(select(models.News))
    events = result.scalars().all()
    if not events:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
# get news by id 

@router.get("/news/{id}", response_model= News)
def get_news_id(*, db: Session = Depends(get_db), id: int):
    # create a db query
    result = db.execute(select(models.News).where(models.News.id == id))
    # parse the query
    event = result.scalars().first()
    
    if not event: 
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    
@router.post("/news", response_model=News, status_code=status.HTTP_201_CREATED)
def create_news(*, db: Session = Depends(get_db), news : NewsBase):
    result = db.execute(insert(models.News).values(track = news.track, title = news.title, date = news.date, body = news.body).returning(models.News))
    db.commit()
    event = result.scalars().first()
    if not event: 
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return event


@router.post("/event/{id}", response_model= News, status_code=status.HTTP_201_CREATED)
def update_news(*, db: Session = Depends(get_db), news: NewsBase, id: int): 
    result = db.execute(update(models.News).where(models.News.id == id).values(track = news.track, title = news.title, date = news.date, body = news.body).returning(models.News))
    db.commit()
    event = result.scalars().first()
    if not event: 
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return event



@router.delete("/event/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_news(*, db: Session = Depends(get_db), id: int): 
    result = db.execute(delete(models.Event).returning(models.Event).where(models.Event.id == id))
    db.commit()
    deleted = result.scalar()
    if not deleted:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    