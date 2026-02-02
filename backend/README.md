# PSP Backend

This folder contains a Flask backend and SQLite schema for the PSP (Personal Strategic Plan) app.

Quick start (macOS):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
python -m backend.app
```

API endpoints:
- `POST /api/psps` create a PSP
- `GET /api/psps` list PSPs (sorted by create time desc)
- `GET /api/psps/<id>` get PSP detail with tasks and report
- `POST /api/psps/<id>/tasks` create a task for a PSP
- `PATCH /api/tasks/<id>` update a task
- `DELETE /api/tasks/<id>` delete a task

Notes:
- Database defaults to `sqlite:///./psp.db`.
- Use Alembic for migrations if evolving schema.
