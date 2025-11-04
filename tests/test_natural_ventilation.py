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


# -------------------- Test Title and Main Sections --------------------
def test_nv_title(page: Page):
    """Verify the title and main chart sections are visible"""
    expect(page.get_by_text("Natural Ventilation Potential")).to_be_visible()
    expect(page.locator("#nv-heatmap-chart")).to_be_visible()
    expect(page.locator("#nv-bar-chart")).to_be_visible()


# -------------------- Test Input Controls --------------------
def test_nv_input_controls(page: Page):
    """Check input controls for temperature and dew point filters"""
    expect(page.locator("#nv-dbt-filter")).to_be_visible()
    expect(page.locator("#nv-dpt-filter")).to_be_visible()
    expect(page.locator("#nv-tdb-min-val")).to_be_visible()
    expect(page.locator("#nv-tdb-max-val")).to_be_visible()
    expect(page.locator("#nv-dpt-max-val")).to_be_visible()
    expect(page.locator("#enable-condensation")).to_be_visible()


# -------------------- Test Normalize Switch --------------------
def test_nv_normalize_switch(page: Page):
    """Ensure normalize switch and tooltip are visible"""
    expect(page.get_by_text("Normalize data")).to_be_visible()


# -------------------- Test Apply Filter Button Interaction --------------------
def test_nv_apply_filter(page: Page):
    """Click Apply Filter and check that the heatmap updates"""
    button = page.locator("#nv-dbt-filter")
    expect(button).to_be_visible()
    button.click()
    expect(page.locator("#nv-heatmap-chart")).to_be_visible()


# -------------------- Test Condensation Checkbox Interaction --------------------
def test_nv_condensation_checkbox(page: Page):
    """Toggle condensation checkbox and verify dew point filter enables"""
    checkbox = page.locator("input#enable-condensation")
    button = page.locator("#nv-dpt-filter")

    expect(button).to_be_disabled()

    checkbox.click()
    expect(button).to_be_enabled()

    checkbox.click()
    expect(button).to_be_disabled()
