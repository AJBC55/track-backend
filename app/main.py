from fastapi import FastAPI
from .database import  engine
from .routers import event, news

from . import models




models.Base.metadata.create_all(bind=engine)




app = FastAPI()
app.include_router(event.router)
app.include_router(news.router)




@app.get("/home")
def home():
    return {"data": "home"}


