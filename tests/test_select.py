import pytest
from playwright.sync_api import Page, expect
from utils import upload_epw_file


@pytest.fixture(scope="function", autouse=True)
def setup(page: Page, base_url):
    page.goto(f"{base_url}")
    yield


# -------------------- Test Select Page Core Elements --------------------
def test_select_core_elements(page: Page):
    """Verify that the Select Weather File page loads and shows basic elements"""
    # Main text and alerts
    expect(page.locator("text=Select an EPW file from your computer")).to_be_visible()
    expect(page.locator("#alert")).to_contain_text("upload an EPW file")

    # Upload button
    upload_button = page.locator("#upload-data-button")
    expect(upload_button).to_be_visible()
    expect(upload_button).to_contain_text("Select an EPW file")

    # Upload section container
    expect(page.locator("#upload-data")).to_be_visible()


# -------------------- Test EPW Upload and Map Rendering --------------------
def test_upload_and_map_rendering(page: Page):
    """
    Simulate uploading an EPW file, verify success message and map rendering
    """
    upload_epw_file(page)

    # Confirm success alert
    alert_box = page.locator("#alert")
    expect(alert_box).to_be_visible()
    expect(alert_box).to_contain_text("EPW was successfully loaded!")

    # Map rendered after file upload
    map_container = page.locator("#map-container")
    expect(map_container).to_be_visible()
