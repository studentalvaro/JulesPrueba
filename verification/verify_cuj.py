import subprocess
import time
import os
from playwright.sync_api import sync_playwright

def run_cuj(page):
    page.goto("http://localhost:8002")
    page.wait_for_timeout(500)

    # Scroll to the baker section
    page.locator("#baker").scroll_into_view_if_needed()
    page.wait_for_timeout(500)

    # Click the cookie 15 times to unlock the first achievement and show debounce
    cookie = page.locator("#cookie")
    for i in range(15):
        cookie.click()
        # No wait here to simulate rapid clicking

    page.wait_for_timeout(500)

    # Take screenshot showing 15 cookies and first achievement unlocked
    page.screenshot(path="/home/jules/verification/screenshots/verification.png")

    # Wait for debounce to trigger (1s)
    print("Waiting for debounce...")
    page.wait_for_timeout(1500)

    # Reload to show persistence worked
    page.reload()
    page.wait_for_timeout(1000)
    page.locator("#baker").scroll_into_view_if_needed()
    page.wait_for_timeout(500)

    # Final state
    page.screenshot(path="/home/jules/verification/screenshots/final_state.png")
    page.wait_for_timeout(1000)

if __name__ == "__main__":
    # Start server
    server_process = subprocess.Popen(["python3", "-m", "http.server", "8002"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)

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
        server_process.terminate()
        server_process.wait()
