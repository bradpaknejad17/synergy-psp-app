from datetime import date, datetime
from enum import Enum
from sqlalchemy import Column, Integer, String, Date, DateTime, Float, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class CategoryEnum(str, Enum):
    FAMILY_FRIENDS = "Family & Friends"
    FINANCE = "Finance"
    CAREER_EDUCATION = "Career/Education"
    WELL_BEING = "Well-Being"
    COMMUNITY = "Community"

class PSP(Base):
    __tablename__ = 'psp'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    contract = Column(String)
    vision = Column(String)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(String, default='ACTIVE', nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    tasks = relationship('Task', back_populates='psp', cascade='all, delete-orphan')

    def days_total(self):
        return (self.end_date - self.start_date).days

    def days_remaining(self):
        return (self.end_date - date.today()).days

class Task(Base):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True)
    psp_id = Column(Integer, ForeignKey('psp.id'), nullable=False)
    description = Column(String)
    category = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    due_date = Column(Date)
    completed_value = Column(Float, default=0)
    target_value = Column(Float, default=0)
    unit = Column(String)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    psp = relationship('PSP', back_populates='tasks')

    def days_remaining(self):
        if not self.due_date:
            return None
        return (self.due_date - date.today()).days

    def percent_complete(self):
        try:
            if self.target_value == 0:
                return 0.0
            return min(100.0, (self.completed_value / self.target_value) * 100.0)
        except Exception:
            return 0.0
