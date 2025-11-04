import pytest
from playwright.sync_api import Page, expect
from utils import upload_epw_file, open_tab


@pytest.fixture(scope="function", autouse=True)
def setup(page: Page, base_url):
    """Setup: Go to base URL, upload EPW file, and open Outdoor page"""
    page.goto(base_url)
    upload_epw_file(page)
    open_tab(page, "Outdoor Comfort")
    yield


# -------------------- Test Title & Section Headings --------------------
def test_outdoor_titles(page: Page):
    """Verify key outdoor section titles are visible"""
    expect(page.get_by_text("Select a scenario:")).to_be_visible()
    expect(page.get_by_text("UTCI heatmap chart")).to_be_visible()
    expect(page.get_by_text("UTCI thermal stress chart")).to_be_visible()
    expect(page.get_by_text("Normalize data")).to_be_visible()
    expect(page.get_by_text("The Best Weather Condition is:")).to_be_visible()


# -------------------- Test Image & Switch Components --------------------
def test_outdoor_image_and_switch(page: Page):
    """Verify that image and switch controls are visible"""
    expect(page.locator("#image-selection")).to_be_visible()


# -------------------- Test Charts Rendering --------------------
def test_outdoor_charts_render(page: Page):
    """Ensure that main UTCI charts are rendered"""
    expect(page.locator("#utci-heatmap")).to_be_visible()
    expect(page.locator("#utci-category-heatmap")).to_be_visible()
    expect(page.locator("#utci-summary-chart")).to_be_visible()


# -------------------- Test Dropdown Interaction --------------------
def test_dropdown_interaction(page: Page):
    """Switch scenario from dropdown and verify chart reloads"""
    dropdown = page.locator("#outdoor-dropdown")
    dropdown.click()
    page.get_by_text("UTCI: Sun & no Wind", exact=True)
    expect(page.locator("#utci-heatmap")).to_be_visible()
    expect(page.locator("#utci-category-heatmap")).to_be_visible()
    expect(page.locator("#utci-summary-chart")).to_be_visible()
