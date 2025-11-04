import pytest
from playwright.sync_api import Page, expect
from utils import upload_epw_file


@pytest.fixture(scope="function", autouse=True)
def setup(page: Page, base_url):
    page.goto(f"{base_url}")
    yield


# -------------------- Test Page Load --------------------
def test_select_page_loads(page: Page):
    """Verify that the Select Weather File page loads successfully"""
    expect(page.locator("text=Select an EPW file from your computer")).to_be_visible()
    expect(page.locator("#upload-data")).to_be_visible()
    expect(page.locator("#alert")).to_contain_text("upload an EPW file")


# -------------------- Test Upload Button Visible --------------------
def test_upload_button_visible(page: Page):
    """Ensure the upload EPW button is visible"""
    upload_button = page.locator("#upload-data-button")
    expect(upload_button).to_be_visible()
    expect(upload_button).to_contain_text("Select an EPW file")


# -------------------- Test Upload EPW File --------------------
def test_upload_epw_file_success(page: Page):
    """
    Simulate uploading an EPW file and verify success alert appears.
    This test uses helper 'upload_epw_file' from utils.py.
    """
    upload_epw_file(page)
    alert_box = page.locator("#alert")
    expect(alert_box).to_be_visible()
    expect(alert_box).to_contain_text("EPW was successfully loaded!")


# -------------------- Test Map Renders --------------------
def test_map_renders(page: Page):
    """Verify that the map (epw_location.json plot) renders properly"""
    map_container = page.locator("#tab-one-map")
    expect(map_container).to_be_visible()
