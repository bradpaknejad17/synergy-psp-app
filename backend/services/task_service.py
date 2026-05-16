from typing import Any, Dict, Optional

from ..repository.task_repo import TaskRepository


class TaskService:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    def create(self, psp_id: int, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return self.repo.create_task(psp_id, payload)

    def create_bulk(self, psp_id: int, payload: list) -> Optional[list]:
        return self.repo.create_tasks_bulk(psp_id, payload)

    def update(self, task_id: int, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return self.repo.update_task(task_id, payload)

    def delete(self, task_id: int) -> bool:
        return self.repo.delete_task(task_id)
