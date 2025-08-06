# TrailCamPro

A minimal FastAPI application for uploading trail camera images and auto-tagging wildlife.

## Features
- User registration and login with JWT authentication
- Authenticated camera creation and image upload (supports multiple files)
- Browse images per camera with simple filtering
- Search media across cameras by species, time of day, date range, or keyword
- Simple AI-based tagging using filename cues and brightness heuristic

## Development
Install dependencies:
```bash
pip install -r requirements.txt
```

Run the app:
```bash
uvicorn app.main:app --reload
```

Use the API:

- Register a user: `POST /users/register`
- Obtain a token: `POST /users/login`
- Include the token in `Authorization: Bearer <token>` header when creating cameras and uploading images.`
- Upload images: `POST /cameras/{camera_id}/upload` (use `files` field and send multiple files if desired)
- Search media: `GET /media/search` with optional query params `camera_id`, `species`, `time_of_day`, `start_date`, `end_date`, `q`

Run tests:
```bash
pytest
```
