import os
import sys
from fastapi.testclient import TestClient
import time
from datetime import datetime, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app
from app.database import Base, engine

Base.metadata.create_all(bind=engine)
client = TestClient(app)


def test_register_and_login():
    response = client.post("/users/register", json={"username": "test", "password": "test"})
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "test"

    response = client.post("/users/login", data={"username": "test", "password": "test"})
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_upload_images(tmp_path):
    client.post("/users/register", json={"username": "u2", "password": "pw"})
    token = client.post("/users/login", data={"username": "u2", "password": "pw"}).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    cam = client.post("/cameras/", json={"name": "cam1"}, headers=headers).json()
    img_path = tmp_path / "deer_day.jpg"
    with open(img_path, "wb") as f:
        f.write(os.urandom(1024))
    with open(img_path, "rb") as f:
        files = {"files": ("deer_day.jpg", f, "image/jpeg")}
        response = client.post(f"/cameras/{cam['id']}/upload", files=files, headers=headers)
    assert response.status_code == 200
    data = response.json()[0]
    assert data["filename"] == "deer_day.jpg"
    list_resp = client.get(f"/cameras/{cam['id']}/images", headers=headers)
    assert list_resp.status_code == 200
    assert len(list_resp.json()) == 1


def test_media_search(tmp_path):
    client.post("/users/register", json={"username": "u3", "password": "pw"})
    token = client.post("/users/login", data={"username": "u3", "password": "pw"}).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    cam = client.post("/cameras/", json={"name": "cam1"}, headers=headers).json()

    deer_path = tmp_path / "deer_8.jpg"
    with open(deer_path, "wb") as f:
        f.write(os.urandom(1024))
    with open(deer_path, "rb") as f:
        files = {"files": ("deer_8.jpg", f, "image/jpeg")}
        first = client.post(f"/cameras/{cam['id']}/upload", files=files, headers=headers).json()[0]

    time.sleep(1)
    turkey_path = tmp_path / "turkey_night.jpg"
    with open(turkey_path, "wb") as f:
        f.write(os.urandom(1024))
    with open(turkey_path, "rb") as f:
        files = {"files": ("turkey_night.jpg", f, "image/jpeg")}
        client.post(f"/cameras/{cam['id']}/upload", files=files, headers=headers)

    # Search by species
    resp = client.get("/media/search", headers=headers, params={"species": "turkey"})
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1 and data[0]["filename"] == "turkey_night.jpg"

    # Keyword search
    resp = client.get("/media/search", headers=headers, params={"q": "8-point"})
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1 and data[0]["filename"] == "deer_8.jpg"

    # Date range filter
    start = (datetime.fromisoformat(first["uploaded_at"]) + timedelta(seconds=0.5)).isoformat()
    resp = client.get("/media/search", headers=headers, params={"start_date": start})
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1 and data[0]["filename"] == "turkey_night.jpg"
