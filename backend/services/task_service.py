from typing import Any, Dict, Optional

from ..api.responses.task_response import TaskDTO
from ..mappers.task_mapper import to_dto
from ..repository.task_repo import TaskRepository


class TaskService:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    def create(self, psp_id: int, payload: Dict[str, Any]) -> Optional[TaskDTO]:
        task = self.repo.create_task(psp_id, payload)
        if not task:
            return None
        return to_dto(task)

    def create_bulk(self, psp_id: int, payload: list) -> Optional[list[TaskDTO]]:
        tasks = self.repo.create_tasks_bulk(psp_id, payload)
        if tasks is None:
            return None
        return [to_dto(task) for task in tasks]

    def update(self, task_id: int, payload: Dict[str, Any]) -> Optional[TaskDTO]:
        task = self.repo.update_task(task_id, payload)
        if not task:
            return None
        return to_dto(task)

    def delete(self, task_id: int) -> bool:
        return self.repo.delete_task(task_id)
