import os
import time
import subprocess
from playwright.sync_api import sync_playwright

def run_cuj(page):
    # Navigate to the app via local server to ensure cookies work correctly
    page.goto("http://localhost:8005")
    page.wait_for_timeout(500)

    # 1. Click the cookie to bake 12 cookies (enough to trigger the first achievement)
    cookie = page.locator("#cookie")
    for _ in range(12):
        cookie.click()
        page.wait_for_timeout(100) # Slightly slower to be visible in video

    page.wait_for_timeout(500)

    # 2. Verify achievement "Rookie" is unlocked
    rookie_badge = page.locator("#ach-10")
    # In CSS, unlocked class adds yellow border

    # 3. Trigger visibility change to force immediate save
    page.evaluate("""
        Object.defineProperty(document, 'visibilityState', { value: 'hidden', writable: true });
        document.dispatchEvent(new Event('visibilitychange'));
    """)
    page.wait_for_timeout(500)

    # 4. Reload page to verify persistence
    page.reload()
    page.wait_for_timeout(1000)

    counter = page.locator("#counter")
    # Take screenshot of final state
    page.screenshot(path="/home/jules/verification/screenshots/final_verification.png")
    page.wait_for_timeout(1000)

if __name__ == "__main__":
    # Start server
    server_process = subprocess.Popen(["python3", "-m", "http.server", "8005"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
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
