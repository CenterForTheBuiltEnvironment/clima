import pytest
from playwright.sync_api import Page, expect
from utils import upload_epw_file, open_tab


@pytest.fixture(scope="function", autouse=True)
def setup(page: Page, base_url):
    """Setup: open base URL, upload EPW file, and navigate to /t_rh page"""
    page.goto(base_url)
    upload_epw_file(page)
    open_tab(page, "Temperature and Humidity")
    yield


# -------------------- Test Temperature and Humidity Page Core Elements --------------------
def test_t_rh_core_elements(page: Page):
    """Test visibility of section titles, chart containers, and statistics table"""

    # Section titles
    section_titles = [
        "Yearly Chart",
        "Daily chart",
        "Heatmap chart",
        "Descriptive statistics",
    ]
    for title in section_titles:
        expect(page.get_by_text(title)).to_be_visible()

    # Charts
    chart_ids = ["#yearly-chart", "#daily", "#heatmap"]
    for cid in chart_ids:
        expect(page.locator(cid)).to_be_visible()

    # Table
    table = page.locator("#table-tmp-hum")
    expect(table).to_be_visible()

    expected_columns = ["month", "mean", "min", "max", "std", "Jun", "Year"]
    for col in expected_columns:
        expect(table).to_contain_text(col)


# -------------------- Test Variable Switching --------------------
def test_switch_variable_and_rerender(page: Page):
    """Switch variable in dropdown and check chart re-renders"""
    dropdown = page.locator("#dropdown")
    dropdown.click()
    page.get_by_text("Relative humidity").click()
    # Re-check visibility of charts after switching variable
    expect(page.locator("#yearly-chart")).to_be_visible()
    expect(page.locator("#daily")).to_be_visible()
    expect(page.locator("#heatmap")).to_be_visible()


# -------------------- Test Global/Local System Toggle --------------------
def test_banner_unit_switch(page: Page):
    """
    Verify that the banner radio buttons (Global/Local) correctly toggle.
    """
    nav_controls = page.locator("#nav-group-controls")
    nav_controls.click(force=True)

    # Click the "Global" option
    global_button = page.get_by_text("Global", exact=True)
    global_button.scroll_into_view_if_needed()
    global_button.wait_for(state="visible")
    global_button.click(force=True)

    expect(page.get_by_text("-40", exact=False)).to_be_visible()
