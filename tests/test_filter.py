import re
from typing import List, Tuple, Optional

import pytest
from playwright.sync_api import Page, expect, Locator

from utils import upload_epw_file


def ensure_local_mode_and_invert_off(page: Page):
    """Ensure 'Local' mode is active and 'Invert' is off."""
    try:
        page.get_by_text("Local", exact=True).click()
    except Exception:
        pass
    try:
        invert = (
            page.get_by_text("Invert", exact=True)
            .locator("..")
            .locator("input[type=checkbox]")
        )
        if invert.is_checked():
            invert.uncheck()
    except Exception:
        pass


def open_tools_menu_and_filter_section(page: Page):
    apply_btn = page.get_by_text("Apply month and hour filter", exact=False)
    expect(apply_btn.first).to_be_visible()
    ensure_local_mode_and_invert_off(page)


BASELINE_MONTH: Tuple[int, int] = (1, 12)
BASELINE_HOUR: Tuple[int, int] = (0, 24)
NARROW_MONTHS: List[Tuple[int, int]] = [(1, 4), (8, 12)]
NARROW_HOURS: List[Tuple[int, int]] = [(0, 3), (18, 24)]


def _sliders_in_group(page: Page, group_label: str) -> List[Locator]:
    """Return the two sliders for a given group using global order: [month_lo, month_hi, hour_lo, hour_hi]."""
    sliders = page.get_by_role("slider")
    n = sliders.count()
    if n >= 4:
        if "month" in group_label.lower():
            return [sliders.nth(0), sliders.nth(1)]
        if "hour" in group_label.lower():
            return [sliders.nth(2), sliders.nth(3)]
    return [sliders.nth(0), sliders.nth(1)] if n >= 2 else []


def _read_slider_value(slider: Locator) -> Optional[float]:
    """Read a slider's numeric value."""
    for attr in ("aria-valuenow", "value"):
        v = slider.get_attribute(attr)
        if v:
            try:
                return float(v)
            except ValueError:
                continue
    return None


def _keyboard_move_to(
    slider: Locator, target: float, vmin: float, vmax: float, step: float = 1.0
):
    """Move a slider thumb to target using only keyboard arrows."""
    slider.scroll_into_view_if_needed()
    slider.focus()
    current = _read_slider_value(slider)
    if current is None:
        slider.press("Home")
        current = vmin
    diff = target - current
    key = "ArrowRight" if diff > 0 else "ArrowLeft"
    steps = int(abs(diff) / max(step, 1))
    steps = min(steps, 200)
    for _ in range(steps):
        slider.press(key)


def _set_range(
    page: Page,
    group_label: str,
    target_lo: float,
    target_hi: float,
    domain_lo: float,
    domain_hi: float,
    step: float,
):
    sliders = _sliders_in_group(page, group_label)
    if len(sliders) < 2:
        return
    lo, hi = sliders[0], sliders[1]
    _keyboard_move_to(lo, target_lo, domain_lo, domain_hi, step)
    _keyboard_move_to(hi, target_hi, domain_lo, domain_hi, step)


def set_month_range(page: Page, m_start: int, m_end: int):
    _set_range(page, "Month Range", m_start, m_end, 1, 12, step=1.0)


def set_hour_range(page: Page, h_start: int, h_end: int):
    _set_range(page, "Hour Range", h_start, h_end, 0, 24, step=1.0)


def _click_apply(page: Page):
    """Click the 'Apply' button."""
    try:
        page.get_by_role(
            "button", name=re.compile("Apply month and hour filter", re.I)
        ).first.click()
    except Exception:
        page.get_by_text("Apply month and hour filter", exact=False).first.click()


def apply_filter(page: Page, month_range: Tuple[int, int], hour_range: Tuple[int, int]):
    """Apply the selected filter settings."""
    set_month_range(page, month_range[0], month_range[1])
    set_hour_range(page, hour_range[0], hour_range[1])
    _click_apply(page)


def _chart_state_hash(page: Page, chart_selector: str) -> str:
    """Generate a simple hash from chart inner HTML."""
    node = page.locator(chart_selector).first
    if not node.is_visible():
        node.scroll_into_view_if_needed()
    html = node.inner_html()
    return str(hash(html))


def _wait_dom_change(page: Page, chart_selector: str, prev_html: str):
    """
    Wait until the target chart element's innerHTML changes from prev_html.
    """
    page.wait_for_function(
        "(args) => { const [sel, prev] = args; const el = document.querySelector(sel); return el && el.innerHTML !== prev; }",
        arg=[chart_selector, prev_html],
    )


def assert_chart_changes_by_three_steps(page: Page, chart_selector: str):
    """Test chart reactivity across month/hour/both filter changes."""
    base_hash = _chart_state_hash(page, chart_selector)
    base_html = page.locator(chart_selector).first.inner_html()

    changed = False
    for months in NARROW_MONTHS:
        apply_filter(page, months, BASELINE_HOUR)
        _wait_dom_change(page, chart_selector, base_html)
        base_html = page.locator(chart_selector).first.inner_html()
        if _chart_state_hash(page, chart_selector) != base_hash:
            changed = True
            break

    if not changed:
        for hours in NARROW_HOURS:
            apply_filter(page, BASELINE_MONTH, hours)
            _wait_dom_change(page, chart_selector, base_html)
            base_html = page.locator(chart_selector).first.inner_html()
            if _chart_state_hash(page, chart_selector) != base_hash:
                changed = True
                break

    if not changed:
        months, hours = NARROW_MONTHS[0], NARROW_HOURS[0]
        apply_filter(page, months, hours)
        _wait_dom_change(page, chart_selector, base_html)
        page.locator(chart_selector).first.inner_html()
        if _chart_state_hash(page, chart_selector) != base_hash:
            changed = True

    assert changed, (
        f"Chart did not change after filter steps for selector {chart_selector}"
    )


PAGES = [
    ("summary", "/summary", ["#degree-days-chart-wrapper"]),
    ("t_rh", "/t-rh", ["#heatmap", "#daily", "#yearly-chart"]),
    ("sun", "/sun", ["#custom-sunpath", "#monthly-solar", "#cloud-cover"]),
    ("wind", "/wind", ["#wind-rose", "#wind-speed", "#wind-direction"]),
    ("psy", "/psy-chart", ["#psych-chart"]),
    ("outdoor", "/outdoor", ["#utci-heatmap", "#utci-summary-chart"]),
    ("explorer", "/explorer", ["#yearly-explore", "#query-daily", "#custom-heatmap"]),
]


@pytest.fixture(scope="function", autouse=True)
def _bootstrap_each(page: Page, base_url: str):
    page.goto(base_url)
    upload_epw_file(page)
    yield


@pytest.mark.parametrize("page_name,path,selectors", PAGES, ids=[p[0] for p in PAGES])
def test_time_filter_affects_page(
    page: Page, base_url: str, page_name: str, path: str, selectors: List[str]
):
    """Verify that charts react to month/hour filters (no screenshot, no timeout)."""
    page.goto(f"{base_url}{path}")
    open_tools_menu_and_filter_section(page)

    target = None
    for sel in selectors:
        loc = page.locator(sel).first
        try:
            loc.scroll_into_view_if_needed()
        except Exception:
            pass
        if loc.is_visible():
            target = sel
            break
    if not target:
        target = selectors[0]
        page.locator(target).first.wait_for(state="visible")

    assert_chart_changes_by_three_steps(page, target)
