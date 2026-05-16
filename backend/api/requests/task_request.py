from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


class CreateTaskRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    description: Optional[str] = None
    category: str = Field(..., min_length=1, description="The category of the task")
    start_date: date = Field(..., description="The start date of the task")
    due_date: Optional[date] = Field(default=None, description="The due date of the task")
    completed_value: float = Field(default=0, description="The completed value of the task")
    target_value: float = Field(default=0, description="The target value of the task")
    unit: Optional[str] = Field(default=None, description="The unit of the task")
    completed: bool = Field(default=False, description="Whether the task is complete")

    @model_validator(mode="after")
    def validate_date_range(self) -> "CreateTaskRequest":
        if self.due_date and self.due_date < self.start_date:
            raise ValueError("due_date must be on or after start_date")
        return self


class UpdateTaskRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    description: Optional[str] = None
    category: Optional[str] = Field(default=None, min_length=1)
    start_date: Optional[date] = None
    due_date: Optional[date] = None
    completed_value: Optional[float] = None
    target_value: Optional[float] = None
    unit: Optional[str] = None
    completed: Optional[bool] = None

    @model_validator(mode="after")
    def validate_date_range(self) -> "UpdateTaskRequest":
        if self.start_date and self.due_date and self.due_date < self.start_date:
            raise ValueError("due_date must be on or after start_date")
        return self
