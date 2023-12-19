from fastui import AnyComponent
from fastui import components as c
from fastui.events import GoToEvent


def demo_page(*components: AnyComponent, title: str | None = None) -> list[AnyComponent]:
    return [
        c.PageTitle(text=f'Decision App: {title}' if title else 'Decision App'),
        c.Navbar(
            title='Decision App',
            title_event=GoToEvent(url='/'),
            links=[
                c.Link(
                    components=[c.Text(text='Decisions')],
                    on_click=GoToEvent(url='/decisions'),
                    active='startswith:/components',
                ),
                c.Link(
                    components=[c.Text(text='Archive')],
                    on_click=GoToEvent(url='/archive'),
                    active='startswith:/table',
                ),
                c.Link(
                    components=[c.Text(text='Review')],
                    on_click=GoToEvent(url='/review'),
                    active='startswith:/forms',
                ),
            ],
        ),
        c.Page(
            components=[
                *((c.Heading(text=title),) if title else ()),
                *components,
            ],
        ),
    ]
