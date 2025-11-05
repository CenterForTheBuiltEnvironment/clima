import pytest
from playwright.sync_api import Page, expect
from utils import upload_epw_file, open_tab


@pytest.fixture(scope="function", autouse=True)
def setup(page: Page, base_url):
    """Setup: open base URL, upload EPW file, and navigate to /summary page"""
    page.goto(base_url)
    upload_epw_file(page)
    open_tab(page, "Climate Summary")
    yield


# -------------------- Test Section Titles --------------------
def test_summary_titles(page: Page):
    """Verify all main section headers are visible"""
    expect(page.get_by_role("heading", name="Download")).to_be_visible()
    expect(page.get_by_text("Heating and Cooling Degree Days")).to_be_visible()
    expect(page.get_by_text("Climate Profiles")).to_be_visible()


# -------------------- Test Location Info Load --------------------
def test_location_info_loaded(page: Page):
    """Check if location info section displays properly"""
    """Verify that location info section shows correct values"""
    info_section = page.locator("#location-info")
    expect(info_section).to_be_visible()
    expected_texts = [
        "Location: Bologna Marconi AP, ITA",
        "Longitude: 11.2969",
        "Latitude: 44.5308",
        "Elevation above sea level: 37.0 m",
        "This file is based on data collected between 2004 and 2018",
        "Köppen-Geiger climate zone: Cfa. Humid subtropical, no dry season.",
        "Average yearly temperature: 14.5 °C",
        "Hottest yearly temperature (99%): 34.0 °C",
        "Coldest yearly temperature (1%): -2.0 °C",
        "Annual cumulative horizontal solar radiation: 1546.12 kWh/m2",
        "Percentage of diffuse horizontal solar radiation: 39.4 %",
    ]
    for text in expected_texts:
        expect(info_section).to_contain_text(text)

    expect(page.locator("#world-map")).to_be_visible()


# -------------------- Test Download Buttons --------------------
def test_download_buttons(page: Page, tmp_path):
    """Verify that both download buttons are visible and clickable"""

    # Locate both download buttons on the page
    epw_button = page.get_by_role("button", name="Download EPW")
    clima_button = page.get_by_role("button", name="Download Clima dataframe")

    # Ensure the buttons are visible
    expect(epw_button).to_be_visible()
    expect(clima_button).to_be_visible()


# -------------------- Test Degree Day Setpoints and Chart --------------------
def test_degree_day_chart_visible(page: Page):
    """Ensure degree day chart and input controls are visible"""
    expect(page.locator("#input-hdd-set-point")).to_be_visible()
    expect(page.locator("#input-cdd-set-point")).to_be_visible()
    expect(page.locator("#submit-set-points")).to_be_visible()
    expect(page.locator("#degree-days-chart-wrapper")).to_be_visible()


# -------------------- Test Climate Profile Graphs --------------------
def test_climate_profile_graphs(page: Page):
    """Verify that the four climate profile graphs are visible"""
    expect(page.locator("#temp-profile-graph")).to_be_visible()
    expect(page.locator("#humidity-profile-graph")).to_be_visible()
    expect(page.locator("#solar-radiation-graph")).to_be_visible()
    expect(page.locator("#wind-speed-graph")).to_be_visible()


# -------------------- Test SI/IP System Toggle --------------------
def test_unit_switch(page: Page):
    """
    Verify that the banner radio buttons (SI/IP) correctly toggle.
    """
    nav_controls = page.locator("#nav-group-controls")
    nav_controls.click(force=True)

    # Click the "IP" option
    ip_button = page.get_by_text("IP", exact=True)
    expect(ip_button).to_be_visible()
    ip_button.scroll_into_view_if_needed()
    ip_button.wait_for(state="visible")
    ip_button.click(force=True)

    info_section = page.locator("#location-info")
    expect(info_section.get_by_text("°F")).to_be_visible
    expect(info_section.get_by_text("ft")).to_be_visible
    expect(info_section.get_by_text("kBtu/ft2")).to_be_visible