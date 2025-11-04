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


# -------------------- Test Outdoor Page Core Elements --------------------
def test_outdoor_core_elements(page: Page):
    """Verify core UI components (titles, image, charts) are visible"""
    # Section titles
    expected_texts = [
        "Select a scenario:",
        "UTCI heatmap chart",
        "UTCI thermal stress chart",
        "Normalize data",
        "The Best Weather Condition is:",
    ]
    for text in expected_texts:
        expect(page.get_by_text(text)).to_be_visible()

    # Image and switch
    expect(page.locator("#image-selection")).to_be_visible()

    # Charts
    chart_ids = [
        "#utci-heatmap",
        "#utci-category-heatmap",
        "#utci-summary-chart",
    ]
    for cid in chart_ids:
        expect(page.locator(cid)).to_be_visible()


# -------------------- Test Dropdown Interaction --------------------
def test_outdoor_dropdown_interaction(page: Page):
    """Switch scenario in dropdown and verify all charts reload"""
    dropdown = page.locator("#outdoor-dropdown")
    dropdown.click()
    page.get_by_text("UTCI: Sun & no Wind", exact=True).click()

    for chart_id in [
        "#utci-heatmap",
        "#utci-category-heatmap",
        "#utci-summary-chart",
    ]:
        expect(page.locator(chart_id)).to_be_visible()
