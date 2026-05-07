import os
from playwright.sync_api import sync_playwright, expect

def verify_cuj():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Using record_video_dir to capture the session
        context = browser.new_context(record_video_dir="/home/jules/verification/videos/")
        page = context.new_page()

        current_dir = os.path.dirname(os.path.abspath(__file__))
        app_dir = os.path.dirname(current_dir)
        index_path = os.path.join(app_dir, "index.html")
        file_url = f"file://{index_path}"

        page.goto(file_url)

        # Click until some achievements are unlocked
        cookie = page.locator("#cookie")
        for _ in range(15):
            cookie.click()

        # Verify counter
        counter = page.locator("#counter")
        expect(counter).to_have_text("Cookies Baked: 15")

        # Verify achievement state
        rookie = page.locator("#ach-10")
        expect(rookie).to_have_class("badge unlocked")

        # Take a final screenshot
        page.screenshot(path="/home/jules/verification/final_verification.png")

        context.close()
        browser.close()

if __name__ == "__main__":
    if not os.path.exists("/home/jules/verification/videos/"):
        os.makedirs("/home/jules/verification/videos/", exist_ok=True)
    verify_cuj()
