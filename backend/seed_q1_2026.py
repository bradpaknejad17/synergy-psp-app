from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Optional

from .repository.db import SessionLocal, init_db
from .models.models import PSP, Task


@dataclass(frozen=True)
class SeedTask:
    description: str
    category: str
    start_date: date
    due_date: Optional[date]
    completed_value: float = 0.0
    target_value: float = 0.0
    unit: Optional[str] = None


def _should_mark_completed(completed_value: float, target_value: float) -> bool:
    if target_value <= 0:
        return False
    return completed_value >= target_value


def seed_q1_2026() -> int:
    init_db()

    psp_title = "PSP Q1 2026"
    psp_start = date(2026, 1, 1)
    psp_end = date(2026, 3, 31)

    contract = "I am an Authentic, Open, Courageous Leader"
    vision = (
        "To be an impactful and positively influential leader that provides for family,\n"
        "friends, and the community around him\n\n"
        "To responsibly save and invest for the future with the intent to bless future generations with stability, donation, and abundance\n\n"
        "To build and run my own software-based business in an industry or problem space that I care about with my brother and to have the\n"
        "freedom to be my own boss, work alongside great people, and feel deep satisfaction in my work.\n\n"
        "To invest in health and well-being in order to show up in the world with energy, clarity, and enthusiasm that inspires others to pursue their\n"
        "best selves\n\n"
        "To dedicate time and knowledge to empowering others, building a culture of support, resilience, and shared success\n\n"
        "To nurture meaningful bonds with friends/family, building a culture of care and belonging that inspires others to prioritize connection in\n"
        "their own lives."
    )

    tasks: list[SeedTask] = [
        # Family & Friends
        SeedTask(
            description="I have planned and attended at least 1 dinner with Alina and Aman by 2/28/26",
            category="Family & Friends",
            start_date=psp_start,
            due_date=date(2026, 2, 28),
            completed_value=0,
            target_value=1,
            unit="event",
        ),
        SeedTask(
            description="I have planned and attended at least 1 drinks session with Tom/TJ, Rishi, and one other person by 2/28/26",
            category="Family & Friends",
            start_date=psp_start,
            due_date=date(2026, 2, 28),
            completed_value=0,
            target_value=1,
            unit="event",
        ),
        # Finance
        SeedTask(
            description="I have created a budget that states what percent of my income I will invest on a bi-weekly basis by 2/28/26",
            category="Finance",
            start_date=psp_start,
            due_date=date(2026, 2, 28),
            completed_value=0,
            target_value=1,
            unit="budget",
        ),
        SeedTask(
            description="I have increased my personal net worth by at least 2.5% for a total net worth of at least $747,258.825 by 3/31/26",
            category="Finance",
            start_date=psp_start,
            due_date=psp_end,
            completed_value=0,
            target_value=747_258.83,
            unit="USD",
        ),
        SeedTask(
            description="I have transferred my Amazon shares from my Morgan Stanley account to Robinhood by 1/31/26",
            category="Finance",
            start_date=psp_start,
            due_date=date(2026, 1, 31),
            completed_value=0,
            target_value=1,
            unit="transfer",
        ),
        # Career/Education
        SeedTask(
            description="I have landed and accepted a job offer paying at least $215,000 base salary and offering a total compensation of at least $350,000 by 1/25/2026",
            category="Career/Education",
            start_date=psp_start,
            due_date=date(2026, 1, 25),
            completed_value=470_000.00,
            target_value=350_000.00,
            unit="USD",
        ),
        SeedTask(
            description="I have landed a job offer at Brex, Rippling, and ScaleAI by 1/16/2026",
            category="Career/Education",
            start_date=psp_start,
            due_date=date(2026, 1, 16),
            completed_value=1,
            target_value=3,
            unit="offers",
        ),
        # Well-Being - Physical Health/Spiritual
        SeedTask(
            description="I have shed 10 lbs by 3/31/2026",
            category="Well-Being - Physical Health/Spiritual",
            start_date=psp_start,
            due_date=psp_end,
            completed_value=0,
            target_value=15,
            unit="lbs",
        ),
        SeedTask(
            description="I have taken at least a 1 week solo trip by 1/31/2026 to a destination of my choosing and have booked and paid for it by 1/9/2026",
            category="Well-Being - Physical Health/Spiritual",
            start_date=psp_start,
            due_date=date(2026, 1, 9),
            completed_value=1,
            target_value=1,
            unit="trip",
        ),
        SeedTask(
            description="Starting 2/1/26, I am performing at least 15 minutes of cardio 3x per week for a total of 24 cardio sessions by 3/31/2026",
            category="Well-Being - Physical Health/Spiritual",
            start_date=date(2026, 2, 1),
            due_date=psp_end,
            completed_value=0,
            target_value=24,
            unit="sessions",
        ),
        SeedTask(
            description="I have taken at least one weekend trip to Miami, FL solo or with a small group by 3/31/26",
            category="Well-Being - Physical Health/Spiritual",
            start_date=psp_start,
            due_date=psp_end,
            completed_value=0,
            target_value=1,
            unit="trip",
        ),
        # Community
        SeedTask(
            description="I have volunteered via a NY cares initiative at least 3 times by 3/31/2026",
            category="Community",
            start_date=psp_start,
            due_date=psp_end,
            completed_value=0,
            target_value=3,
            unit="times",
        ),
        SeedTask(
            description="Starting 1/1/26 I am donating $200 directly to the homeless or those in need on a monthly basis for a total of $600 donated by 3/31/26",
            category="Community",
            start_date=psp_start,
            due_date=psp_end,
            completed_value=0.0,
            target_value=600.0,
            unit="USD",
        ),
    ]

    with SessionLocal() as session:
        existing = (
            session.query(PSP)
            .filter(PSP.title == psp_title, PSP.start_date == psp_start, PSP.end_date == psp_end)
            .first()
        )
        if existing:
            print(f"Seed skipped: PSP already exists (id={existing.id})")
            return 0

        psp = PSP(
            title=psp_title,
            contract=contract,
            vision=vision,
            start_date=psp_start,
            end_date=psp_end,
            status="ACTIVE",
        )
        session.add(psp)
        session.flush()  # assign psp.id

        for t in tasks:
            task = Task(
                psp_id=psp.id,
                description=t.description,
                category=t.category,
                start_date=t.start_date,
                due_date=t.due_date,
                completed_value=float(t.completed_value),
                target_value=float(t.target_value),
                unit=t.unit,
                completed=bool(_should_mark_completed(float(t.completed_value), float(t.target_value))),
            )
            session.add(task)

        session.commit()

        print(f"Seeded PSP id={psp.id} with {len(tasks)} tasks")
        return 0


if __name__ == "__main__":
    raise SystemExit(seed_q1_2026())

