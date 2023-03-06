# see: https://playwright.dev/python/docs/test-runners
# pytest --browser webkit --headed

import re

import pytest
from decouple import config
from playwright.sync_api import Page, expect

DEBUG = config("DEBUG", default=False, cast=bool)

API_URL = "http://localhost:8501/" if DEBUG else "http://myapp:8501/"


def test_homepage(page: Page):
    page.goto(API_URL)

    # Expect a title "to contain" a substring.
    expect(page).to_have_title(re.compile("overview"))

    # create a locator
    new = page.get_by_role("link", name="new")
    update = page.get_by_role("link", name="update")

    new.click()  # click on the page "new"

    expect(page).to_have_title(re.compile("new"))

    page.screenshot(path="screenshot.png", full_page=True)


@pytest.mark.order(after="test_homepage")
def test_archive_decisions_exist(page: Page):
    page.goto(API_URL)

    archive = page.get_by_role("link", name="archived")

    archive.click()
    # Expect a title "to contain" a substring.
    expect(page).to_have_title(re.compile("archived"))

    # TODO: add a check that the page contains the archived decisions


def test_page_new(page: Page):
    page.goto(API_URL)

    new = page.get_by_role("link", name="new")

    new.click()

    expect(page).to_have_title(re.compile("new"))

    page.get_by_role("textbox", name="Decision Name").fill("Go to sleep?")

    page.get_by_role("button", name="Submit").click()

    page.screenshot(path="screenshot_new.png", full_page=True)


@pytest.mark.order(after="test_page_new")
def test_archive_decision_action(page: Page):
    page.goto(API_URL)

    # Expect a title "to contain" a substring.

    page.get_by_role("combobox", name="Select a decision").fill("Go to sleep?")

    page.get_by_role("button", name="Archive").click()

    page.screenshot(path="screenshot_archive_action.png", full_page=True)
