from typing import Dict, Any, Optional
from datetime import date, datetime
from zoneinfo import ZoneInfo
from ..repository.db import SessionLocal
from ..models.models import Task, PSP
from ..models.schemas import TaskSchema

task_schema = TaskSchema()


def _parse_date(value: str) -> date:
    # assume `value` is an ISO date string (YYYY-MM-DD) or datetime string
    # return a Python date object
    if 'T' in value:
        return datetime.fromisoformat(value).date()
    return date.fromisoformat(value)


def create_task(psp_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
    with SessionLocal() as session:
        p = session.get(PSP, psp_id)
        if not p:
            return None
        t = Task(
            psp_id=psp_id,
            description=data.get('description'),
            category=data['category'],
            start_date=_parse_date(data['start_date']),
            due_date=_parse_date(data.get('due_date')),
            completed_value=data.get('completed_value', 0),
            target_value=data.get('target_value', 0),
            unit=data.get('unit'),
            completed=data.get('completed', False)
        )
        session.add(t)
        session.commit()
        session.refresh(t)
        return task_schema.dump(t)


def create_tasks_bulk(psp_id: int, tasks: list) -> Optional[list]:
    """Create multiple tasks for a PSP in a single transaction.

    `tasks` is a list of dicts with the same fields accepted by `create_task` (without psp_id).
    Returns list of created task dicts, or None if PSP not found.
    """
    with SessionLocal() as session:
        p = session.get(PSP, psp_id)
        if not p:
            return None
        created = []
        objects = []
        for data in tasks:
            t = Task(
                psp_id=psp_id,
                description=data.get('description'),
                category=data.get('category', 'Uncategorized'),
                start_date=_parse_date(data.get('start_date')),
                due_date=_parse_date(data.get('due_date')) if data.get('due_date') else None,
                completed_value=data.get('completed_value', 0),
                target_value=data.get('target_value', 0),
                unit=data.get('unit'),
                completed=data.get('completed', False)
            )
            objects.append(t)
            session.add(t)
        # commit once
        session.commit()
        for t in objects:
            session.refresh(t)
            created.append(task_schema.dump(t))
        return created


def update_task(task_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
    with SessionLocal() as session:
        t = session.get(Task, task_id)
        if not t:
            return None
        # handle date parsing for known date fields
        if 'start_date' in data:
            data['start_date'] = _parse_date(data['start_date'])
        if 'due_date' in data:
            data['due_date'] = _parse_date(data['due_date'])
        for k, v in data.items():
            if hasattr(t, k):
                setattr(t, k, v)
        session.add(t)
        session.commit()
        session.refresh(t)
        return task_schema.dump(t)


def delete_task(task_id: int) -> bool:
    with SessionLocal() as session:
        t = session.get(Task, task_id)
        if not t:
            return False
        session.delete(t)
        session.commit()
        return True
