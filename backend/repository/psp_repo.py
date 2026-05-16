from datetime import date
from typing import Dict, List, Optional

from sqlalchemy.orm import selectinload

from ..persistence.models.db import PSP, PSPStatusEnum
from ..repository.db import SessionLocal


def compute_psp_percent(psp: PSP) -> float:
    tasks = psp.tasks or []
    if not tasks:
        return 0.0

    total_weight = 0.0
    total_completed = 0.0
    for task in tasks:
        target = task.target_value or 0
        completed = task.completed_value or 0
        if target == 0:
            total_weight += 1
            total_completed += 1 if task.completed else 0
        else:
            total_weight += target
            total_completed += min(completed, target)

    if total_weight <= 0:
        return 0.0
    return round((total_completed / total_weight) * 100.0, 2)


def aggregate_by_category(psp: PSP) -> Dict[str, Dict[str, float]]:
    result: Dict[str, Dict[str, float]] = {}
    for task in psp.tasks or []:
        category = task.category or "Uncategorized"
        bucket = result.setdefault(category, {"total": 0, "completed": 0, "percent": 0.0})
        bucket["total"] += 1
        if task.completed:
            bucket["completed"] += 1

    for bucket in result.values():
        total = bucket["total"]
        bucket["percent"] = round((bucket["completed"] / total) * 100.0, 2) if total else 0.0
    return result


class PSPRepository:
    def create_psp(
        self,
        *,
        title: str,
        contract: Optional[str],
        vision: Optional[str],
        start_date: date,
        end_date: date,
    ) -> PSP:
        with SessionLocal() as session:
            psp = PSP(
                title=title,
                contract=contract,
                vision=vision,
                start_date=start_date,
                end_date=end_date,
            )
            session.add(psp)
            session.commit()
            session.refresh(psp)
            session.expunge(psp)
            return psp

    def list_psps(self, status: Optional[PSPStatusEnum] = None) -> List[PSP]:
        with SessionLocal() as session:
            query = session.query(PSP)
            if status is not None:
                query = query.filter(PSP.status == status)
            psps = query.order_by(PSP.created_at.desc()).all()
            for psp in psps:
                session.expunge(psp)
            return psps

    def get_psp_with_tasks(self, psp_id: int) -> Optional[PSP]:
        with SessionLocal() as session:
            psp = (
                session.query(PSP)
                .options(selectinload(PSP.tasks))
                .filter(PSP.id == psp_id)
                .one_or_none()
            )
            if not psp:
                return None
            session.expunge(psp)
            return psp

    def delete_by_id(self, psp_id: int) -> Optional[PSP]:
        with SessionLocal() as session:
            psp = session.get(PSP, psp_id)
            if not psp:
                return None
            psp.status = PSPStatusEnum.DELETED
            session.add(psp)
            session.commit()
            session.refresh(psp)
            session.expunge(psp)
            return psp
