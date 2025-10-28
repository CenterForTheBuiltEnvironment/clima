import pytest
from playwright.sync_api import Page, expect
from utils import upload_epw_file, open_tab


@pytest.fixture(scope="function", autouse=True)
def setup(page: Page, base_url):
    """Setup: Go to base URL, upload EPW file, and open Explorer page"""
    page.goto(base_url)
    upload_epw_file(page)
    open_tab(page, "Data Explorer")
    yield


# -------------------- Test Title & Section Headings --------------------
def test_explorer_titles(page: Page):
    """Check key titles and headings are visible"""
    expect(page.get_by_text("Select a variable:")).to_be_visible()
    expect(page.get_by_text("Yearly chart")).to_be_visible()
    expect(page.get_by_text("Daily chart")).to_be_visible()
    expect(page.get_by_text("Heatmap chart")).to_be_visible()
    expect(page.get_by_text("Descriptive statistics")).to_be_visible()
    expect(page.get_by_text("Customizable heatmap")).to_be_visible()
    expect(page.get_by_text("More charts")).to_be_visible()


# -------------------- Test Section One Charts --------------------
def test_section_one_charts(page: Page):
    """Check if Section One charts render properly"""
    expect(page.locator("#yearly-explore")).to_be_visible()
    expect(page.locator("#query-daily")).to_be_visible()
    expect(page.locator("#query-heatmap")).to_be_visible()
    expect(page.locator("#table-data-explorer")).to_be_visible()


# -------------------- Test Section Two Charts --------------------
def test_section_two_charts(page: Page):
    """Ensure Section Two charts and summary elements appear"""
    expect(page.locator("#custom-heatmap")).to_be_visible()


# -------------------- Test Section Three Controls --------------------
def test_section_three_controls(page: Page):
    """Check 'More charts' section inputs and controls"""
    expect(page.locator("#explorer-sec3-var-x-dropdown")).to_be_visible()
    expect(page.locator("#explorer-sec3-var-y-dropdown")).to_be_visible()
    expect(page.locator("#explorer-sec3-colorby-dropdown")).to_be_visible()


# -------------------- Test Section Three Charts --------------------
def test_section_three_charts(page: Page):
    """Check if 2-variable and 3-variable graphs are rendered"""
    expect(page.locator("#three-var")).to_be_visible()
    expect(page.locator("#two-var")).to_be_visible()


# -------------------- Test Dropdown Interaction --------------------
def test_explorer_dropdown_interaction(page: Page):
    """Switch variable in dropdown and verify chart reloads"""
    dropdown = page.locator("#sec1-var-dropdown")
    dropdown.click()
    options = page.locator(".VirtualizedSelectOption")
    assert options.count() > 0
    options.filter(has_text="Relative humidity").first.click()
    expect(page.locator("#yearly-explore")).to_be_visible()
    expect(page.locator("#query-heatmap")).to_be_visible()
