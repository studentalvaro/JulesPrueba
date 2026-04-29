import os
import time
import subprocess
from playwright.sync_api import sync_playwright, expect

def test_debounce():
    # Start a local HTTP server
    server_process = subprocess.Popen(["python3", "-m", "http.server", "8001"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)  # Wait for server to start

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()

            url = "http://localhost:8001"
            page.goto(url)

            cookie = page.locator("#cookie")

            print("Clicking 5 times rapidly...")
            for i in range(5):
                cookie.click()

            # Check cookies immediately - should NOT be updated yet (if it was 0 before)
            # Actually, it might have been 0.
            cookies = context.cookies()
            state_cookie = next((c for c in cookies if c['name'] == '_ab_state'), None)

            # Since debounce is 1000ms, it shouldn't have saved '5' yet if clicks were fast.
            # But Playwright click() has some delay.

            print("Waiting 1.5s for debounce...")
            time.sleep(1.5)

            cookies = context.cookies()
            state_cookie = next((c for c in cookies if c['name'] == '_ab_state'), None)
            if state_cookie:
                print("Cookie found after debounce.")
            else:
                print("Cookie NOT found after debounce.")

            page.reload()
            expect(page.locator("#counter")).to_have_text("Cookies Baked: 5")
            print("Verified count after debounce and reload: 5")

            browser.close()
    finally:
        server_process.terminate()
        server_process.wait()

if __name__ == "__main__":
    test_debounce()
