import enum
from datetime import date
from typing import Annotated, Literal, TypeAlias

from fastapi import UploadFile
from fastui.forms import FormFile
from pydantic import BaseModel, EmailStr, SecretStr, field_validator
from pydantic import Field as PydanticField
from pydantic_core import PydanticCustomError


class SizeModel(BaseModel):
    width: int = PydanticField(description="This is a field of a nested model")
    height: int = PydanticField(description="This is a field of a nested model")


class BigModel(BaseModel):
    name: str | None = PydanticField(
        None,
        description="This field is not required, it must start with a capital letter if provided",
    )
    profile_pic: Annotated[
        UploadFile, FormFile(accept="image/*", max_size=16_000)
    ] = PydanticField(
        description="Upload a profile picture, must not be more than 16kb"
    )
    profile_pics: Annotated[
        list[UploadFile], FormFile(accept="image/*")
    ] | None = PydanticField(None, description="Upload multiple images")
    dob: date = PydanticField(
        title="Date of Birth",
        description="Your date of birth, this is required hence bold",
    )
    human: bool | None = PydanticField(
        None,
        title="Is human",
        description="Are you human?",
        json_schema_extra={"mode": "switch"},
    )
    size: SizeModel

    @field_validator("name")
    def name_validator(cls, v: str | None) -> str:
        if v and v[0].islower():
            raise PydanticCustomError("lower", "Name must start with a capital letter")
        return v


FormKind: TypeAlias = Literal["login", "select", "big"]


class LoginForm(BaseModel):
    email: EmailStr = PydanticField(
        title="Email Address", description="Try 'x@y' to trigger server side validation"
    )
    password: SecretStr


class ToolEnum(str, enum.Enum):
    hammer = "hammer"
    screwdriver = "screwdriver"
    saw = "saw"
    claw_hammer = "claw_hammer"


class SelectForm(BaseModel):
    select_single: ToolEnum = PydanticField(title="Select Single")
    select_multiple: list[ToolEnum] = PydanticField(title="Select Multiple")
    search_select_single: str = PydanticField(
        json_schema_extra={"search_url": "/api/forms/search"}
    )
    search_select_multiple: list[str] = PydanticField(
        json_schema_extra={"search_url": "/api/forms/search"}
    )
