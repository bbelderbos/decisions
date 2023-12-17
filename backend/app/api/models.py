from datetime import date
from enum import Enum

from sqlmodel import Field, SQLModel


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
    archived: bool = False


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
