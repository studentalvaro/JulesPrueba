import os
from playwright.sync_api import sync_playwright, expect

def test_cookie_clicker():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Construct the file path to index.html
        current_dir = os.path.dirname(os.path.abspath(__file__))
        app_dir = os.path.dirname(current_dir)
        index_path = os.path.join(app_dir, "index.html")
        file_url = f"file://{index_path}"

        print(f"Navigating to {file_url}")
        page.goto(file_url)

        # Verify initial state
        counter = page.locator("#counter")
        expect(counter).to_have_text("Cookies Baked: 0")
        print("Initial counter state verified: 0")

        # Click the cookie 10 times
        cookie = page.locator("#cookie")
        for i in range(10):
            cookie.click()

        # Verify final state
        expect(counter).to_have_text("Cookies Baked: 10")
        print("Final counter state verified: 10")

        # Take a screenshot
        screenshot_path = os.path.join(current_dir, "screenshot.png")
        page.screenshot(path=screenshot_path, full_page=True)
        print(f"Screenshot saved to {screenshot_path}")

        browser.close()

if __name__ == "__main__":
    test_cookie_clicker()
