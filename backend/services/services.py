from datetime import date
from sqlalchemy.orm import Session
from ..models.models import PSP, Task

def compute_task_percent(task: Task) -> float:
    return task.percent_complete()

def compute_psp_percent(session: Session, psp: PSP) -> float:
    # Simple unweighted percent across tasks (by completed_value/target_value)
    tasks = psp.tasks
    if not tasks:
        return 0.0
    total_weight = 0.0
    total_completed = 0.0
    for t in tasks:
        target = t.target_value or 0
        completed = t.completed_value or 0
        if target == 0:
            # treat as count-based: completed counts as 1 if completed flag true
            total_weight += 1
            total_completed += 1 if t.completed else 0
        else:
            total_weight += target
            total_completed += min(completed, target)
    try:
        return round((total_completed / total_weight) * 100.0, 2) if total_weight > 0 else 0.0
    except ZeroDivisionError:
        return 0.0

def aggregate_by_category(psp: PSP):
    result = {}
    for t in psp.tasks:
        cat = t.category or 'Uncategorized'
        if cat not in result:
            result[cat] = {'total': 0, 'completed': 0, 'percent': 0.0}
        result[cat]['total'] += 1
        if t.completed:
            result[cat]['completed'] += 1
    for k,v in result.items():
        v['percent'] = round((v['completed'] / v['total']) * 100.0, 2) if v['total'] > 0 else 0.0
    return result
