import pytest
from playwright.sync_api import Page, expect
from utils import upload_epw_file, open_tab


@pytest.fixture(scope="function", autouse=True)
def setup(page: Page, base_url):
    """Setup: Go to base URL, upload EPW, and open /psy-chart page"""
    page.goto(base_url)
    upload_epw_file(page)
    open_tab(page, "Psychrometric Chart")
    yield


# -------------------- Test Page Title --------------------
def test_psy_title(page: Page):
    """Check if main Psy Chart title is visible"""
    expect(page.get_by_role("heading", name="Psychrometric Chart")).to_be_visible()


# -------------------- Test Dropdowns and Sliders --------------------
def test_psy_controls_visible(page: Page):
    """Check all interactive inputs are visible"""
    expect(page.locator("#psy-var-dropdown")).to_be_visible()
    expect(page.locator("#psy-min-val")).to_be_visible()
    expect(page.locator("#psy-max-val")).to_be_visible()
    expect(page.get_by_role("button", name="Apply filter")).to_be_visible()


# -------------------- Test Psy Chart Render --------------------
def test_psy_chart_rendered(page: Page):
    """Check that the psy chart is rendered"""
    expect(page.locator("#psych-chart")).to_be_visible()


# -------------------- Test Dropdown Interaction --------------------
def test_dropdown_change_triggers_chart(page: Page):
    """Switch dropdown to another variable and check chart still renders"""
    dropdown = page.locator("#psy-color-by-dropdown")
    dropdown.click()
    page.get_by_text("Dry bulb temperature").click()
    expect(page.locator("#psych-chart")).to_be_visible()
