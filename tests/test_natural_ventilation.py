import pytest
from playwright.sync_api import Page, expect
from utils import upload_epw_file, open_tab


@pytest.fixture(scope="function", autouse=True)
def setup(page: Page, base_url):
    """Setup: open app, upload EPW file, and go to Natural Ventilation tab"""
    page.goto(base_url)
    upload_epw_file(page)
    open_tab(page, "Natural Ventilation")
    yield


# -------------------- Test Core Elements --------------------
def test_nv_core_elements(page: Page):
    """Verify title, charts, filters, and switch are visible"""

    # Main title and charts
    expect(page.get_by_text("Natural Ventilation Potential")).to_be_visible()
    expect(page.locator("#nv-heatmap-chart")).to_be_visible()
    expect(page.locator("#nv-bar-chart")).to_be_visible()

    # Filters and inputs
    element_ids = [
        "#nv-dbt-filter",
        "#nv-dpt-filter",
        "#nv-tdb-min-val",
        "#nv-tdb-max-val",
        "#nv-dpt-max-val",
        "#enable-condensation",
    ]
    for eid in element_ids:
        expect(page.locator(eid)).to_be_visible()

    # Switch label
    expect(page.get_by_text("Normalize data")).to_be_visible()


# -------------------- Test Filter Button Triggers Chart --------------------
def test_nv_apply_filter(page: Page):
    """Click Dry Bulb filter and verify heatmap still renders"""
    button = page.locator("#nv-dbt-filter")
    button.click()
    expect(page.locator("#nv-heatmap-chart")).to_be_visible()


# -------------------- Test Condensation Toggle Effect --------------------
def test_nv_condensation_checkbox_toggle(page: Page):
    """Toggling checkbox should enable/disable dew point filter"""
    checkbox = page.locator("input#enable-condensation")
    dewpoint_button = page.locator("#nv-dpt-filter")

    expect(dewpoint_button).to_be_disabled()
    checkbox.click()
    expect(dewpoint_button).to_be_enabled()
    checkbox.click()
    expect(dewpoint_button).to_be_disabled()
