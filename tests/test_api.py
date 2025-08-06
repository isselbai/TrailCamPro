import os
import sys
from fastapi.testclient import TestClient

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
