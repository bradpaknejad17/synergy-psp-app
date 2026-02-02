from typing import List, Dict, Any, Optional
from datetime import date, datetime
from zoneinfo import ZoneInfo
from ..repository.db import SessionLocal
from ..models.models import PSP
from ..models.schemas import PSPSchema
from ..services.services import compute_psp_percent, aggregate_by_category

psp_schema = PSPSchema()


def _parse_date(value: str) -> date:
    # assume `value` is an ISO date string (YYYY-MM-DD) or datetime string
    # return a Python date object
    if 'T' in value:
        return datetime.fromisoformat(value).date()
    return date.fromisoformat(value)


def create_psp(data: Dict[str, Any]) -> Dict[str, Any]:
    with SessionLocal() as session:
        p = PSP(
            title=data['title'],
            contract=data.get('contract'),
            vision=data.get('vision'),
            start_date=_parse_date(data['start_date']),
            end_date=_parse_date(data['end_date'])
        )
        session.add(p)
        session.commit()
        session.refresh(p)
        return psp_schema.dump(p)

def list_psps() -> List[Dict[str, Any]]:
    from datetime import date
    with SessionLocal() as session:
        psps = session.query(PSP).order_by(PSP.created_at.desc()).all()
        out = []
        for p in psps:
            d = psp_schema.dump(p)
            # timeline calculations
            try:
                total_days = p.days_total()
            except Exception:
                total_days = None
            try:
                days_remaining = p.days_remaining()
            except Exception:
                days_remaining = None
            # days elapsed (clamped)
            if total_days is None or total_days <= 0:
                timeline_percent = 0.0
            else:
                days_elapsed = (date.today() - p.start_date).days
                if days_elapsed < 0:
                    days_elapsed = 0
                if days_elapsed > total_days:
                    days_elapsed = total_days
                timeline_percent = round((days_elapsed / total_days) * 100.0, 2)
            d['days_remaining'] = days_remaining
            d['timeline_percent'] = timeline_percent
            out.append(d)
        return out

def get_psp_with_tasks(psp_id: int) -> Dict[str, Any]:
    with SessionLocal() as session:
        p = session.get(PSP, psp_id)
        if not p:
            return None
        # prepare tasks list
        tasks = [
            {
                'id': t.id,
                'description': t.description,
                'category': t.category,
                'start_date': t.start_date.isoformat(),
                'due_date': t.due_date.isoformat() if t.due_date else None,
                'completed_value': t.completed_value,
                'target_value': t.target_value,
                'unit': t.unit,
                'completed': bool(t.completed)
            }
            for t in p.tasks
        ]
        report = {
            'percent_complete': compute_psp_percent(session, p),
            'by_category': aggregate_by_category(p),
            'days_remaining': p.days_remaining()
        }
        out = psp_schema.dump(p)
        out['tasks'] = tasks
        out['report'] = report
        return out
