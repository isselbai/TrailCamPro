from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class ImageBase(BaseModel):
    filename: str

class ImageCreate(ImageBase):
    pass

class Image(ImageBase):
    id: int
    uploaded_at: datetime
    species: Optional[str] = None
    antler_class: Optional[str] = None
    time_of_day: Optional[str] = None

    class Config:
        orm_mode = True

class CameraBase(BaseModel):
    name: str

class CameraCreate(CameraBase):
    pass

class Camera(CameraBase):
    id: int
    images: List[Image] = []

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    role: str
    cameras: List[Camera] = []

    class Config:
        orm_mode = True
