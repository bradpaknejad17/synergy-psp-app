import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..models.models import Base

DATABASE_URL = os.getenv('PSP_DATABASE_URL', 'sqlite:///./psp.db')

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if DATABASE_URL.startswith('sqlite') else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    # Create tables based on SQLAlchemy models
    Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    init_db()
    print('Initialized database at', DATABASE_URL)
