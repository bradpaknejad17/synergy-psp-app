from typing import Any, Dict, Optional

from ..persistence.models.db import PSP, Task
from ..persistence.models.schemas import TaskSchema
from ..repository.db import SessionLocal
from ..utils.date_utils import parse_date

task_schema = TaskSchema()


def create_task(psp_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    with SessionLocal() as session:
        psp = session.get(PSP, psp_id)
        if not psp:
            return None

        task = Task(
            psp_id=psp_id,
            description=data.get("description"),
            category=data["category"],
            start_date=parse_date(data["start_date"]),
            due_date=parse_date(data["due_date"]) if data.get("due_date") else None,
            completed_value=data.get("completed_value", 0),
            target_value=data.get("target_value", 0),
            unit=data.get("unit"),
            completed=data.get("completed", False),
        )
        session.add(task)
        session.commit()
        session.refresh(task)
        return task_schema.dump(task)


def create_tasks_bulk(psp_id: int, tasks: list) -> Optional[list]:
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
                start_date=parse_date(data["start_date"]),
                due_date=parse_date(data["due_date"]) if data.get("due_date") else None,
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
            created.append(task_schema.dump(task))
        return created


def update_task(task_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    with SessionLocal() as session:
        task = session.get(Task, task_id)
        if not task:
            return None

        if "start_date" in data and data["start_date"] is not None:
            data["start_date"] = parse_date(data["start_date"])
        if "due_date" in data:
            data["due_date"] = parse_date(data["due_date"]) if data["due_date"] else None

        for key, value in data.items():
            if hasattr(task, key):
                setattr(task, key, value)

        session.add(task)
        session.commit()
        session.refresh(task)
        return task_schema.dump(task)


def delete_task(task_id: int) -> bool:
    with SessionLocal() as session:
        task = session.get(Task, task_id)
        if not task:
            return False
        session.delete(task)
        session.commit()
        return True
