from datetime import date, datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict


class PSPDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    contract: Optional[str] = None
    vision: Optional[str] = None
    start_date: date
    end_date: date
    status: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    days_remaining: Optional[int] = None
    timeline_percent: float = 0.0


class TaskDTO(BaseModel):
    id: int
    description: Optional[str] = None
    category: str
    start_date: date
    due_date: Optional[date] = None
    completed_value: float = 0.0
    target_value: float = 0.0
    unit: Optional[str] = None
    completed: bool = False


class PSPReportDTO(BaseModel):
    percent_complete: float
    by_category: Dict[str, Dict[str, float]]
    days_remaining: Optional[int] = None


class PSPDetailDTO(PSPDTO):
    tasks: List[TaskDTO]
    report: PSPReportDTO


class CreatePSPResponse(BaseModel):
    data: PSPDTO


class ListPSPResponse(BaseModel):
    data: List[PSPDTO]
