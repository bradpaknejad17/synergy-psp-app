from datetime import date

from ..api.responses.psp_response import PSPDTO, PSPDetailDTO, PSPReportDTO, TaskDTO
from ..persistence.models.db import PSP, Task


def to_dto(psp: PSP) -> PSPDTO:
    total_days = psp.days_total()
    days_remaining = psp.days_remaining()
    if total_days <= 0:
        timeline_percent = 0.0
    else:
        days_elapsed = (date.today() - psp.start_date).days
        days_elapsed = min(max(days_elapsed, 0), total_days)
        timeline_percent = round((days_elapsed / total_days) * 100.0, 2)

    return PSPDTO(
        id=psp.id,
        title=psp.title,
        contract=psp.contract,
        vision=psp.vision,
        start_date=psp.start_date,
        end_date=psp.end_date,
        status=psp.status,
        created_at=psp.created_at,
        updated_at=psp.updated_at,
        days_remaining=days_remaining,
        timeline_percent=timeline_percent,
    )


def task_to_dto(task: Task) -> TaskDTO:
    return TaskDTO(
        id=task.id,
        description=task.description,
        category=task.category,
        start_date=task.start_date,
        due_date=task.due_date,
        completed_value=task.completed_value,
        target_value=task.target_value,
        unit=task.unit,
        completed=bool(task.completed),
    )


def to_detail_dto(
    psp: PSP,
    *,
    percent_complete: float,
    by_category: dict,
) -> PSPDetailDTO:
    base = to_dto(psp)
    return PSPDetailDTO(
        **base.model_dump(),
        tasks=[task_to_dto(task) for task in psp.tasks],
        report=PSPReportDTO(
            percent_complete=percent_complete,
            by_category=by_category,
            days_remaining=psp.days_remaining(),
        ),
    )
