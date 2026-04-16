from playwright.sync_api import Page, expect, sync_playwright
import os

def test_achievement_unlock(page: Page):
    # 1. Arrange: Go to the app
    url = f"file://{os.getcwd()}/index.html"
    page.goto(url)

    # 2. Act: Click the cookie 10 times to unlock the first achievement
    cookie = page.locator("#cookie")
    for _ in range(10):
        cookie.click()

    # 3. Assert: Confirm the first achievement is unlocked
    rookie_badge = page.locator("#ach-10")
    expect(rookie_badge).to_have_class("badge unlocked")

    # Scroll to the achievements section
    rookie_badge.scroll_into_view_if_needed()

    # 4. Screenshot: Capture the unlocked achievement
    page.screenshot(path="verification/achievement_unlocked.png")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            test_achievement_unlock(page)
        finally:
            browser.close()
