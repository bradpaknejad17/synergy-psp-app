from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class TaskDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    psp_id: int
    description: Optional[str] = None
    category: str
    start_date: date
    due_date: Optional[date] = None
    completed_value: float = 0.0
    target_value: float = 0.0
    unit: Optional[str] = None
    completed: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
