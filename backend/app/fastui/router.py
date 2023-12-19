
from app.api.database import get_session
from app.api.models import Decision
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastui import AnyComponent, FastUI, prebuilt_html
from fastui import components as c
from fastui.components.display import DisplayLookup, DisplayMode
from fastui.events import BackEvent, GoToEvent
from sqlmodel import Session, select

from .models import BigModel, FormKind, LoginForm, SelectForm
from .shared import demo_page

router = APIRouter()

@router.get('/api/', response_model=FastUI, response_model_exclude_none=True)
def api_index() -> list[AnyComponent]:
    # language=markdown
    markdown = """This app provides you with guidance on how to prepare, make and review crucial decisions."""
    return demo_page(c.Markdown(text=markdown), title="Home")


@router.get("/api/decisions", response_model=FastUI, response_model_exclude_none=True)
def decisions_table(*, session: Session = Depends(get_session)) -> list[AnyComponent]:
    """
    Show a table of four users, `/api` is the endpoint the frontend will connect to
    when a user visits `/` to fetch components to render.
    """
    decisions = session.exec(select(Decision)).all()

    return demo_page(
        c.Table[
            Decision
        ](  # c.Table is a generic component parameterized with the model used for rows
            data=decisions,
            # define two columns for the table
            columns=[
                DisplayLookup(
                    field="name", on_click=GoToEvent(url="/decision/{id}/")
                ),
                DisplayLookup(field="id"),
                DisplayLookup(field="time_made", mode=DisplayMode.date),
                DisplayLookup(field="status"),
            ],
        ),
        title="Decisions"
        )


@router.get(
    "/api/decision/{user_id}/", response_model=FastUI, response_model_exclude_none=True
)
def decision_profile(
    user_id: int, session: Session = Depends(get_session)
) -> list[AnyComponent]:
    """
    User profile page, the frontend will fetch this when the user visits `/user/{id}/`.
    """

    decisions = session.exec(select(Decision)).all()

    try:
        user = next(u for u in decisions if u.id == user_id)
    except StopIteration:
        raise HTTPException(status_code=404, detail="Decision not found")
    return [
        c.Page(
            components=[
                c.Heading(text=user.name, level=2),
                c.Link(components=[c.Text(text="Back")], on_click=BackEvent()),
                c.Details(data=user),
            ]
        ),
    ]



@router.get("/content/{kind}", response_model=FastUI, response_model_exclude_none=True)
def form_content(kind: FormKind):
    match kind:
        case "login":
            return [
                c.Heading(text="Login Form", level=2),
                c.Paragraph(text="Simple login form with email and password."),
                c.ModelForm[LoginForm](submit_url="/api/forms/login"),
            ]
        case "select":
            return [
                c.Heading(text="Select Form", level=2),
                c.Paragraph(text="Form showing different ways of doing select."),
                c.ModelForm[SelectForm](submit_url="/api/forms/select"),
            ]
        case "big":
            return [
                c.Heading(text="Large Form", level=2),
                c.Paragraph(text="Form with a lot of fields."),
                c.ModelForm[BigModel](submit_url="/api/forms/big"),
            ]

@router.get("/{path:path}")
async def html_landing() -> HTMLResponse:
    """Simple HTML page which serves the React app, comes last as it matches all paths."""
    return HTMLResponse(prebuilt_html(title="FastUI: Decisions"))
