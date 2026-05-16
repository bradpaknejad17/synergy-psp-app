# PSP Backend

This folder contains a Flask backend and SQLite schema for the PSP (Personal Strategic Plan) app.

Quick start (macOS):

```bash
cd /path/to/synergy-psp-app
python3 -m venv .venv
python3 -m venv backend/.venv
source backend/.venv/bin/activate
pip install -r backend/requirements.txt
python -m backend.app
```

If the virtualenv already exists:

```bash
cd /path/to/synergy-psp-app
source backend/.venv/bin/activate
python -m backend.app
```

Production-style run command:

```bash
cd /path/to/synergy-psp-app
source backend/.venv/bin/activate
gunicorn 'backend.wsgi:app' --bind 0.0.0.0:5000
```

Why this works:
- Run from the repository root so Python can import the `backend` package.
- Use `python -m backend.app` for local development.
- Use `gunicorn 'backend.wsgi:app'` for a production WSGI server.

API endpoints:
- `POST /api/psps` create a PSP
- `GET /api/psps` list PSPs (sorted by create time desc)
- `GET /api/psps/<id>` get PSP detail with tasks and report
- `POST /api/psps/<id>/tasks` create a task for a PSP
- `PATCH /api/psps/<id>/tasks/<task_id>` update a task for a PSP
- `DELETE /api/psps/<id>/tasks/<task_id>` delete a task for a PSP

Notes:
- Database defaults to `sqlite:///./psp.db`.
- SQL bootstrap lives at `backend/persistence/migrations/init.sql`.
- Use Alembic for migrations if evolving schema.
