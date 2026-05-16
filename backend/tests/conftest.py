from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app import create_app
from backend.persistence.models.db import Base
from backend.repository import db as repo_db


@pytest.fixture
def client(tmp_path: Path):
    db_path = tmp_path / "test.db"
    database_url = f"sqlite:///{db_path}"
    engine = create_engine(
        database_url,
        connect_args={"check_same_thread": False},
    )
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    repo_db.DATABASE_URL = database_url
    repo_db.engine = engine
    repo_db.SessionLocal = session_local

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as test_client:
        yield test_client

    Base.metadata.drop_all(bind=engine)
    engine.dispose()
