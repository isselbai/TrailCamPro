from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pathlib import Path

from .. import models, schemas, utils, auth
from ..database import get_db

router = APIRouter(prefix="/cameras", tags=["cameras"])


def save_upload(file: UploadFile, dest: Path) -> Path:
    with dest.open("wb") as buffer:
        buffer.write(file.file.read())
    return dest


@router.post("/", response_model=schemas.Camera)
def create_camera(
    camera: schemas.CameraCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    db_cam = models.Camera(name=camera.name, owner_id=current_user.id)
    db.add(db_cam)
    db.commit()
    db.refresh(db_cam)
    return db_cam


@router.post("/{camera_id}/upload", response_model=List[schemas.Image])
def upload_images(
    camera_id: int,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    camera = db.query(models.Camera).get(camera_id)
    if not camera or camera.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Camera not found")
    saved = []
    Path("uploads").mkdir(exist_ok=True)
    for upload in files:
        path = Path("uploads") / upload.filename
        save_upload(upload, path)
        species, antler, tod = utils.analyze_image(path)
        img = models.Image(filename=upload.filename, camera_id=camera_id, species=species, antler_class=antler, time_of_day=tod)
        db.add(img)
        db.commit()
        db.refresh(img)
        saved.append(img)
    return saved


@router.get("/{camera_id}/images", response_model=List[schemas.Image])
def list_images(
    camera_id: int,
    species: Optional[str] = None,
    time_of_day: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    camera = db.query(models.Camera).get(camera_id)
    if not camera or camera.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Camera not found")
    query = db.query(models.Image).filter(models.Image.camera_id == camera_id)
    if species:
        query = query.filter(models.Image.species == species)
    if time_of_day:
        query = query.filter(models.Image.time_of_day == time_of_day)
    return query.all()
