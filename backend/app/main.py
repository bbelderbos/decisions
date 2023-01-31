from __future__ import annotations

from datetime import date
from enum import Enum

from fastapi import FastAPI, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


class Status(str, Enum):
    Open = "Open"
    Made = "Made"
    Reviewed = "Reviewed"


class DecisionBase(SQLModel):
    name: str
    state_emotional: str
    situation: str
    problem_statement: str
    variables: str
    complications: str
    alternatives: str
    outcome_ranges: str
    expected_with_probabilities: str
    outcome: str
    # next fields are not required for initial create
    time_made: date | None
    time_reviewed: date | None
    status: Status | None = Status.Open
    review: str | None
    rating: int | None = Field(None, gt=0, le=10)


class Decision(DecisionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    time_added: date = Field(default_factory=date.today)


class DecisionCreate(DecisionBase):
    pass


class DecisionRead(DecisionBase):
    id: int


class DecisionUpdate(SQLModel):
    time_made: date | None
    time_reviewed: date | None
    status: Status | None = Status.Open
    review: str | None
    rating: int | None = Field(None, gt=0, le=10)


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/decisions/", response_model=list[DecisionRead])
async def get_decisions():
    with Session(engine) as session:
        decisions = session.exec(select(Decision)).all()
        return decisions


@app.get("/decisions/{decision_id}", response_model=DecisionRead)
async def get_decision(decision_id: int):
    with Session(engine) as session:
        decision = session.get(Decision, decision_id)
        if not decision:
            raise HTTPException(status_code=404, detail="Decision not found")
        return decision


@app.post("/decisions/", response_model=Decision)
async def create_decision(decision: DecisionCreate):
    with Session(engine) as session:
        db_decision = Decision.from_orm(decision)
        session.add(db_decision)
        session.commit()
        session.refresh(db_decision)
        return db_decision


@app.put("/decisions/{decision_id}", response_model=Decision)
async def update_decision(decision_id: int, decision: DecisionUpdate):
    with Session(engine) as session:
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
