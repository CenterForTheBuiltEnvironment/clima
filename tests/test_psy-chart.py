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


# -------------------- Test Psy Page Core Elements --------------------
def test_psy_core_elements(page: Page):
    """Verify page title, controls, and chart are visible"""
    # Title
    expect(page.get_by_role("heading", name="Psychrometric Chart")).to_be_visible()

    # Controls
    expect(page.locator("#psy-var-dropdown")).to_be_visible()
    expect(page.locator("#psy-min-val")).to_be_visible()
    expect(page.locator("#psy-max-val")).to_be_visible()
    expect(page.get_by_role("button", name="Apply filter")).to_be_visible()

    # Chart
    expect(page.locator("#psych-chart")).to_be_visible()


# -------------------- Test Interaction: Dropdown Switch --------------------
def test_dropdown_change_triggers_chart(page: Page):
    """Switch dropdown to another variable and ensure chart re-renders"""
    dropdown = page.locator("#psy-color-by-dropdown")
    dropdown.click()
    page.get_by_text("Dry bulb temperature").click()

    # After dropdown change, chart should still be visible
    expect(page.locator("#psych-chart")).to_be_visible()
