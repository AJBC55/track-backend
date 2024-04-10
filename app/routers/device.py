from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import insert, update

router = APIRouter(prefix="/device", tags=["device operations"])
from app.database import get_db
from app.skema import DeviceCreate, DeviceOut, DeviceToken, User
from app import models
from app.oauth2 import get_current_user


@router.post("", response_model= DeviceOut())
def create_device(*, device_data: DeviceCreate, db: Session = Depends(get_db)):
      # database query 
      result = db.execute(insert(models.Device).values(device_id = device_data.device_id, is_android = device_data.is_android).returning(models.Device))
      device = result.scalars().first()
      if not device:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
      return device 


@router.put("/set-token")
def set_device_token(*, device_token: DeviceToken, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
      result = db.execute(update(models.Device.token).where(device_token.device_id == models.Device.device_id).values(token = device_token.token).returning(models.Device.token))
      db.commit()
      token = result.scalars().one()
      if not token:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="could not save token")
      return {"token": token}