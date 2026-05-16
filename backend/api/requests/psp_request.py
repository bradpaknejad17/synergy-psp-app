from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


class CreatePSPRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(..., min_length=1, max_length=255, description="The title of the PSP")
    contract: Optional[str] = Field(default=None, max_length=255, description="The contract of the PSP")
    vision: Optional[str] = Field(default=None, max_length=255, description="The vision of the PSP")
    start_date: date = Field(..., description="The start date of the PSP")
    end_date: date = Field(..., description="The end date of the PSP")

    @model_validator(mode="after")
    def validate_date_range(self) -> "CreatePSPRequest":
        if self.end_date < self.start_date:
            raise ValueError("end_date must be on or after start_date")
        return self

