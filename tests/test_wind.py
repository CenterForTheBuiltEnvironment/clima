import pytest
from playwright.sync_api import Page, expect
from utils import upload_epw_file, open_tab


@pytest.fixture(scope="function", autouse=True)
def setup(page: Page, base_url):
    """Setup: open base URL, upload EPW file, and navigate to /wind page"""
    page.goto(base_url)
    upload_epw_file(page)
    open_tab(page, "Wind")
    yield


# -------------------- Test Wind Page Core Elements --------------------
def test_wind_core_elements(page: Page):
    """Test core visibility and content on Wind page"""

    # Main titles
    for title in ["Annual Wind Rose", "Seasonal Wind Rose", "Daily Wind Rose"]:
        expect(page.get_by_text(title)).to_be_visible()

    # All wind rose charts
    wind_rose_ids = [
        "#wind-rose",
        "#winter-wind-rose",
        "#spring-wind-rose",
        "#summer-wind-rose",
        "#fall-wind-rose",
        "#morning-wind-rose",
        "#noon-wind-rose",
        "#night-wind-rose",
    ]
    for wid in wind_rose_ids:
        expect(page.locator(wid)).to_be_visible()

    # Description texts
    expected_texts = {
        "#winter-wind-rose-text": "Dec and Feb",
        "#spring-wind-rose-text": "Mar and May",
        "#summer-wind-rose-text": "Jun and Aug",
        "#fall-wind-rose-text": "Sep and Dec",
        "#morning-wind-rose-text": "6:00 hours and 13:00 hours",
        "#noon-wind-rose-text": "14:00 hours and 21:00 hours",
        "#night-wind-rose-text": "22:00 hours and 5:00 hours",
    }

    for cid, expected in expected_texts.items():
        expect(page.locator(cid)).to_contain_text(expected)
