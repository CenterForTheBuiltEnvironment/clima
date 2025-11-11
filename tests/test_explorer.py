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


# -------------------- Test Explorer Core Elements --------------------
def test_explorer_core_elements(page: Page):
    """Check key titles and section one & two charts"""
    # Titles
    for text in [
        "Select a variable:",
        "Yearly chart",
        "Daily chart",
        "Heatmap chart",
        "Descriptive statistics",
        "Customizable heatmap",
        "More charts",
    ]:
        expect(page.get_by_text(text)).to_be_visible()
    # Charts
    for chart in [
        "#yearly-explore",
        "#query-daily",
        "#query-heatmap",
        "#table-data-explorer",
        "#custom-heatmap",
    ]:
        expect(page.locator(chart)).to_be_visible()


# -------------------- Test Section Three --------------------
def test_explorer_section_three(page: Page):
    """Section 3 dropdowns and chart visibility"""
    for selector in [
        "#explorer-sec3-var-x-dropdown",
        "#explorer-sec3-var-y-dropdown",
        "#explorer-sec3-colorby-dropdown",
        "#three-var",
        "#two-var",
    ]:
        expect(page.locator(selector)).to_be_visible()


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
