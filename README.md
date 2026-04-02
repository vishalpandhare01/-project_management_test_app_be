# FastAPI + SQLAlchemy + SQLite Setup

## Setup

1. Create Python venv:
   - `python -m venv .venv`
   - `source .venv/Scripts/activate` (Windows: `.venv\Scripts\activate`)
2. Install deps:
   - `pip install -r requirements.txt`
3. Run app:
   - `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`

## API Endpoints

- `POST /users/` (body: `{ "name": "John", "email": "john@example.com" }`)
- `GET /users/`
- `GET /users/{id}`

## Database

- Uses SQLite at `./test.db`
- Models are auto-created on startup via `models.Base.metadata.create_all(bind=engine)`
