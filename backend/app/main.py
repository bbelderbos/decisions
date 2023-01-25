from __future__ import annotations

from datetime import date
from enum import Enum

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()
decisions = {}
DecisionDb = dict[int, "Decision"]


class Status(str, Enum):
    Open = "Open"
    Made = "Made"
    Reviewed = "Reviewed"


class AddDecision(BaseModel):
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


class UpdateDecision(BaseModel):
    time_made: date | None
    time_reviewed: date | None
    status: Status = Status.Open
    review: str | None
    rating: int | None = Field(None, gt=0, le=10)


class Decision(AddDecision, UpdateDecision):
    time_added: date = Field(default_factory=date.today)


@app.get("/decisions/")
async def get_decisions() -> DecisionDb:
    return decisions


@app.get("/decisions/{decision_id}")
async def get_decision(decision_id: int) -> Decision:
    if decision_id not in decisions:
        raise HTTPException(status_code=404, detail="Item not found")
    return decisions[decision_id]


@app.post("/decisions/")
async def create_decision(add_decision: AddDecision) -> Decision:
    next_id = len(decisions) + 1
    decision = Decision(**add_decision.dict())
    decisions[next_id] = decision
    return decision


@app.put("/decisions/{decision_id}")
async def update_decision(
    decision_id: int, update_decision: UpdateDecision
) -> Decision:
    if decision_id not in decisions:
        raise HTTPException(status_code=404, detail="Decision not found")
    decision = decisions[decision_id]
    data = update_decision.dict(exclude_unset=True)
    for key, value in data.items():
        setattr(decision, key, value)
    decisions[decision_id] = decision
    return decision
