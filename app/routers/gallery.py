from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from datetime import datetime

from .. import models, schemas, auth
from ..database import get_db

router = APIRouter(prefix="/media", tags=["media"])

@router.get("/search", response_model=List[schemas.Image])
def search_media(
    camera_id: Optional[int] = None,
    species: Optional[str] = None,
    time_of_day: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    q: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    query = (
        db.query(models.Image)
        .join(models.Camera)
        .filter(models.Camera.owner_id == current_user.id)
    )
    if camera_id is not None:
        query = query.filter(models.Image.camera_id == camera_id)
    if species:
        query = query.filter(models.Image.species == species)
    if time_of_day:
        query = query.filter(models.Image.time_of_day == time_of_day)
    if start_date:
        query = query.filter(models.Image.uploaded_at >= start_date)
    if end_date:
        query = query.filter(models.Image.uploaded_at <= end_date)
    if q:
        pattern = f"%{q}%"
        query = query.filter(
            or_(
                models.Image.species.ilike(pattern),
                models.Image.antler_class.ilike(pattern),
            )
        )
    return query.all()
