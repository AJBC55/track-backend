from fastapi import FastAPI
from .database import  engine
from .routers import event, news, user, login, admin_events
from . import models











#models.Base.metadata.create_all(bind=engine)




app = FastAPI()

app.include_router(event.router)
app.include_router(news.router)
app.include_router(user.router)
app.include_router(login.router)
app.include_router(admin_events.router)




@app.get("/home")
def home():
    return {"data": "home"}


