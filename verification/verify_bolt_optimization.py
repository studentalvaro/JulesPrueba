from playwright.sync_api import sync_playwright
import os
import subprocess
import time

def run_cuj(page):
    # The app uses cookies for persistence, so we need a server
    page.goto("http://localhost:8080")
    page.wait_for_timeout(1000)

    # CUJ: Click the cookie 15 times to unlock the first achievement (10 cookies)
    cookie = page.locator("#cookie")
    counter = page.locator("#counter")

    print(f"Initial state: {counter.inner_text()}")

    for i in range(15):
        cookie.click()
        page.wait_for_timeout(100)

    print(f"State after 15 clicks: {counter.inner_text()}")

    # Take screenshot of the unlocked achievement
    page.screenshot(path="/home/jules/verification/screenshots/achievement_unlocked.png")
    page.wait_for_timeout(1000)

if __name__ == "__main__":
    # Start a simple server
    server = subprocess.Popen(["python3", "-m", "http.server", "8080"])
    time.sleep(2) # Wait for server to start

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                record_video_dir="/home/jules/verification/videos"
            )
            page = context.new_page()
            try:
                run_cuj(page)
            finally:
                context.close()
                browser.close()
    finally:
        server.terminate()
