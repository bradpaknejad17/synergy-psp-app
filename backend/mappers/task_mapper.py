from ..api.responses.task_response import TaskDTO
from ..persistence.models.db import Task


def to_dto(task: Task) -> TaskDTO:
    return TaskDTO(
        id=task.id,
        psp_id=task.psp_id,
        description=task.description,
        category=task.category,
        start_date=task.start_date,
        due_date=task.due_date,
        completed_value=task.completed_value,
        target_value=task.target_value,
        unit=task.unit,
        completed=bool(task.completed),
        created_at=task.created_at,
        updated_at=task.updated_at,
    )
