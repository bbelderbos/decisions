from typing import Annotated

# from app.api.database import get_session
from app.api.models import Decision, DecisionCreate
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastui import AnyComponent, FastUI, prebuilt_html
from fastui import components as c
from fastui.components.display import DisplayLookup, DisplayMode
from fastui.events import BackEvent, GoToEvent
from fastui.forms import FormResponse, fastui_form
from pydantic import BaseModel, EmailStr, Field, SecretStr
from sqlmodel import Session, select

from .shared import demo_page

router = APIRouter()


@router.get("/api/", response_model=FastUI, response_model_exclude_none=True)
def api_index() -> list[AnyComponent]:
    # language=markdown
    markdown = """This app provides you with guidance on how to prepare, make and review crucial decisions."""
    return demo_page(c.Markdown(text=markdown), title="Home")


@router.get('/{path:path}', status_code=404)
async def api_404():
    # so we don't fall through to the index page
    return {'message': 'Not Found'}
