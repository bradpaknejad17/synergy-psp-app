from typing import Any, Dict, Optional

from ..api.requests.task_request import CreateTaskRequest, UpdateTaskRequest
from ..api.responses.task_response import TaskDTO
from ..mappers.task_mapper import to_dto
from ..repository.task_repo import TaskRepository


class TaskService:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    def create(self, psp_id: int, request: CreateTaskRequest) -> Optional[TaskDTO]:
        task = self.repo.create_task(psp_id, request.model_dump(mode="json"))
        if not task:
            return None
        return to_dto(task)

    def create_bulk(self, psp_id: int, requests: list[CreateTaskRequest]) -> Optional[list[TaskDTO]]:
        tasks = self.repo.create_tasks_bulk(
            psp_id,
            [request.model_dump(mode="json") for request in requests],
        )
        if tasks is None:
            return None
        return [to_dto(task) for task in tasks]

    def update(self, psp_id: int, task_id: int, request: UpdateTaskRequest) -> Optional[TaskDTO]:
        task = self.repo.update_task(
            psp_id,
            task_id,
            request.model_dump(mode="json", exclude_none=True),
        )
        if not task:
            return None
        return to_dto(task)

    def delete(self, psp_id: int, task_id: int) -> bool:
        return self.repo.delete_task(psp_id, task_id)
