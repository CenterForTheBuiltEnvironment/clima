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


# -------------------- Test Page Titles --------------------
def test_sun_titles(page: Page):
    """Verify main Sun page section titles"""
    expect(page.get_by_text("Sun path chart")).to_be_visible()
    expect(
        page.get_by_text("Global and Diffuse Horizontal Solar Radiation")
    ).to_be_visible()
    expect(page.get_by_text("Cloud coverage")).to_be_visible()
    expect(page.get_by_text("Daily charts")).to_be_visible()


# -------------------- Test Dropdown Controls --------------------
def test_sun_dropdown_controls(page: Page):
    """Check if all dropdowns for Sun page controls are visible"""
    expect(page.locator("#custom-sun-view-dropdown")).to_be_visible()
    expect(page.locator("#custom-sun-var-dropdown")).to_be_visible()
    expect(page.locator("#sun-explore-dropdown")).to_be_visible()


# -------------------- Test Graph Visibility --------------------
def test_sun_graphs_visible(page: Page):
    """Ensure all main Sun graphs are rendered correctly"""
    expect(page.locator("#custom-sunpath")).to_be_visible()  # Sun path chart
    expect(page.locator("#monthly-solar")).to_be_visible()  # Global & Diffuse
    expect(page.locator("#cloud-cover")).to_be_visible()  # Cloud coverage
    expect(page.locator("#sun-daily")).to_be_visible()  # Daily line chart
    expect(page.locator("#sun-heatmap")).to_be_visible()  # Daily heatmap


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
