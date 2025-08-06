# TrailCamPro

A minimal FastAPI application for uploading trail camera images and auto-tagging wildlife.

## Features
- User registration and login with JWT authentication
- Authenticated camera creation and image upload
- Browse images per camera with simple filtering
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
- Include the token in `Authorization: Bearer <token>` header when creating cameras and uploading images.

Run tests:
```bash
pytest
```
