from datetime import date
from enum import Enum

from sqlmodel import Field, SQLModel


class Status(str, Enum):
    Open = "Open"
    Made = "Made"
    Reviewed = "Reviewed"


class DecisionBase(SQLModel):
    name: str = "example decision"
    state_emotional: str = "curious"
    situation: str = "I have a decision to make"
    problem_statement: str = "limited resources"
    variables: str = "X, Y, Z"
    complications: str = "A is conflicting with B"
    alternatives: str = "C and D"
    outcome_ranges: str = "may lead to E or F"
    expected_with_probabilities: str = "80 E, 20 F"
    outcome: str = "???"
    # next fields are not required for initial create
    time_made: date | None
    time_reviewed: date | None
    status: Status | None = Status.Open
    review: str | None = "good"
    rating: int | None = Field(1, gt=0, le=10)
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
