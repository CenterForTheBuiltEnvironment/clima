from pathlib import Path
from playwright.sync_api import Page, expect


def upload_epw_file(page: Page, filename: str = "test.epw"):
    """
    Upload an EPW file and verify that the success message appears.

    Parameters:
    - page: The Playwright Page object.
    - filename: Path to the EPW file (defaults to tests/test.epw).
    """
    epw_path = Path(filename).resolve()
    page.set_input_files('input[type="file"]', str(epw_path))

    # Verify that the upload success messages are displayed
    expect(page.get_by_text("The EPW was successfully loaded!")).to_be_visible()
    expect(
        page.get_by_text("Current Location: Bologna Marconi AP, ITA")
    ).to_be_visible()


def open_tab(page: Page, tab_name: str):
    """
    Open a specific tab from the sidebar navigation (default expanded version).
    Works reliably for Mantine NavLink structure.
    """
    # Find the navigation link container whose id starts with "nav-" and text matches
    nav_link = page.locator(f'[id^="nav-"] >> text="{tab_name}"').first

    # Go up to the clickable element (<a> or <button>)
    clickable = nav_link.locator("xpath=ancestor::a[1] | ancestor::button[1]")

    # Scroll and click
    clickable.scroll_into_view_if_needed()
    expect(clickable).to_be_visible()
    clickable.click()
