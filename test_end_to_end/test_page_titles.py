# see: https://playwright.dev/python/docs/test-runners
# pytest --browser webkit --headed

import re

import pytest
from playwright.sync_api import Page, expect


def test_homepage_has_Playwright_in_title_and_get_started_link_linking_to_the_intro_page(page: Page):
    page.goto("http://localhost:8080")
    
    
    # Expect a title "to contain" a substring.
    expect(page).to_have_title(re.compile("overview"))

    # create a locator
    new = page.get_by_role("link", name="new")
    update = page.get_by_role("link", name="update")

    new.click() # click on the page "new"

    expect(page).to_have_title(re.compile("new"))

    page.screenshot(path="screenshot.png", full_page=True)
    