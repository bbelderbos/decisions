from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from .database import create_db_and_tables, get_session
from .models import Decision, DecisionCreate, DecisionRead, DecisionUpdate, Status

router = APIRouter()

@router.on_event("startup")
def on_startup():
    create_db_and_tables()


@router.get("/decisions/", response_model=list[DecisionRead])
async def get_decisions(*, session: Session = Depends(get_session)):
    decisions = session.exec(select(Decision)).all()
    return decisions


@router.get("/decisions/{decision_id}", response_model=DecisionRead)
async def get_decision(*, decision_id: int, session: Session = Depends(get_session)):
    decision = session.get(Decision, decision_id)
    if not decision:
        raise HTTPException(status_code=404, detail="Decision not found")
    return decision


@router.post("/decisions/", response_model=Decision)
async def create_decision(
    *, decision: DecisionCreate, session: Session = Depends(get_session)
):
    db_decision = Decision.from_orm(decision)
    session.add(db_decision)
    session.commit()
    session.refresh(db_decision)
    return db_decision


@router.put("/decisions/{decision_id}", response_model=Decision)
async def update_decision(
    *,
    decision_id: int,
    session: Session = Depends(get_session),
    decision: DecisionUpdate,
):
    db_decision = session.get(Decision, decision_id)
    if not db_decision:
        raise HTTPException(status_code=404, detail="Decision not found")
    decision_data = decision.dict(exclude_unset=True)
    for key, value in decision_data.items():
        setattr(db_decision, key, value)
    session.add(db_decision)
    session.commit()
    session.refresh(db_decision)
    return db_decision


@router.put("/decisions/{decision_id}/archive", response_model=Decision)
async def archive_decision(
    *,
    decision_id: int,
    session: Session = Depends(get_session),
):
    db_decision = session.get(Decision, decision_id)
    if not db_decision:
        raise HTTPException(status_code=404, detail="Decision not found")
    db_decision.archived = True
    session.add(db_decision)
    session.commit()
    session.refresh(db_decision)
    return db_decision


@router.put("/decisions/{decision_id}/unarchive", response_model=Decision)
async def unarchive_decision(
    *,
    decision_id: int,
    session: Session = Depends(get_session),
):
    db_decision = session.get(Decision, decision_id)
    if not db_decision:
        raise HTTPException(status_code=404, detail="Decision not found")
    if db_decision.status == Status.Made:
        raise HTTPException(status_code=400, detail="Decision already made")
    db_decision.archived = False
    session.add(db_decision)
    session.commit()
    session.refresh(db_decision)
    return db_decision
