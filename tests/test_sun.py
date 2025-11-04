import pytest
from playwright.sync_api import Page, expect
from utils import upload_epw_file, open_tab


@pytest.fixture(scope="function", autouse=True)
def setup(page: Page, base_url):
    """Setup: open base URL, upload EPW file, and navigate to /sun page"""
    page.goto(base_url)
    upload_epw_file(page)
    open_tab(page, "Sun and Clouds")
    yield


# -------------------- Test Sun Page Core Elements --------------------
def test_sun_core_elements(page: Page):
    """
    Verify core layout elements are visible: titles, dropdowns, charts.
    """
    # Titles
    expected_titles = [
        "Sun path chart",
        "Global and Diffuse Horizontal Solar Radiation",
        "Cloud coverage",
        "Daily charts",
    ]
    for title in expected_titles:
        expect(page.get_by_text(title)).to_be_visible()

    # Dropdowns
    dropdown_ids = [
        "#custom-sun-view-dropdown",
        "#custom-sun-var-dropdown",
        "#sun-explore-dropdown",
    ]
    for did in dropdown_ids:
        expect(page.locator(did)).to_be_visible()

    # Charts
    chart_ids = [
        "#custom-sunpath",  # Sun path chart
        "#monthly-solar",  # Global & Diffuse
        "#cloud-cover",  # Cloud coverage
        "#sun-daily",  # Daily line chart
        "#sun-heatmap",  # Daily heatmap
    ]
    for cid in chart_ids:
        expect(page.locator(cid)).to_be_visible()


# -------------------- Test Sun Path Chart View and Variable Switching --------------------
def test_sun_path_switch_view_and_variable(page: Page):
    """Switch view and variable in dropdown and check chart re-renders in sun path chart"""
    view_dropdown = page.locator("#custom-sun-view-dropdown")
    view_dropdown.click()
    page.get_by_text("Cartesian").click()
    var_dropdown = page.locator("#custom-sun-var-dropdown")
    var_dropdown.click()
    page.get_by_text("Relative humidity").click()
    expect(page.locator("#custom-sunpath")).to_be_visible()


# -------------------- Test Daily Chart Variable Switching --------------------
def test_daily_switch_variable(page: Page):
    """Switch view and variable in dropdown and check chart re-renders in daily chart"""
    var_dropdown = page.locator("#sun-explore-dropdown")
    var_dropdown.click()
    page.get_by_text("Direct normal illuminance").click()
    expect(page.locator("#sun-daily")).to_be_visible()
