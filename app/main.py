from fastapi import FastAPI
from .routers import users, cameras, gallery
from .database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="TrailCamPro")

app.include_router(users.router)
app.include_router(cameras.router)
app.include_router(gallery.router)
