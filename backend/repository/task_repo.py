from datetime import date, datetime
from typing import Any, Dict, Optional

from ..persistence.models.db import PSP, Task
from ..repository.db import SessionLocal


def _parse_date(value: Optional[str]) -> Optional[date]:
    if not value:
        return None
    if "T" in value:
        return datetime.fromisoformat(value).date()
    return date.fromisoformat(value)


class TaskRepository:
    def create_task(self, psp_id: int, data: Dict[str, Any]) -> Optional[Task]:
        with SessionLocal() as session:
            psp = session.get(PSP, psp_id)
            if not psp:
                return None

            task = Task(
                psp_id=psp_id,
                description=data.get("description"),
                category=data["category"],
                start_date=_parse_date(data["start_date"]),
                due_date=_parse_date(data.get("due_date")),
                completed_value=data.get("completed_value", 0),
                target_value=data.get("target_value", 0),
                unit=data.get("unit"),
                completed=data.get("completed", False),
            )
            session.add(task)
            session.commit()
            session.refresh(task)
            session.expunge(task)
            return task

    def create_tasks_bulk(self, psp_id: int, tasks: list) -> Optional[list[Task]]:
        with SessionLocal() as session:
            psp = session.get(PSP, psp_id)
            if not psp:
                return None

            created = []
            objects = []
            for data in tasks:
                task = Task(
                    psp_id=psp_id,
                    description=data.get("description"),
                    category=data.get("category", "Uncategorized"),
                    start_date=_parse_date(data.get("start_date")),
                    due_date=_parse_date(data.get("due_date")),
                    completed_value=data.get("completed_value", 0),
                    target_value=data.get("target_value", 0),
                    unit=data.get("unit"),
                    completed=data.get("completed", False),
                )
                objects.append(task)
                session.add(task)

            session.commit()
            for task in objects:
                session.refresh(task)
                session.expunge(task)
                created.append(task)
            return created

    def update_task(self, task_id: int, data: Dict[str, Any]) -> Optional[Task]:
        with SessionLocal() as session:
            task = session.get(Task, task_id)
            if not task:
                return None

            if "start_date" in data:
                data["start_date"] = _parse_date(data["start_date"])
            if "due_date" in data:
                data["due_date"] = _parse_date(data["due_date"])

            for key, value in data.items():
                if hasattr(task, key):
                    setattr(task, key, value)

            session.add(task)
            session.commit()
            session.refresh(task)
            session.expunge(task)
            return task

    def delete_task(self, task_id: int) -> bool:
        with SessionLocal() as session:
            task = session.get(Task, task_id)
            if not task:
                return False
            session.delete(task)
            session.commit()
            return True
