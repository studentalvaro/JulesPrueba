import os
import time
import subprocess
from playwright.sync_api import sync_playwright, expect

def test_persistence():
    # Start a local HTTP server
    server_process = subprocess.Popen(["python3", "-m", "http.server", "8000"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)  # Wait for server to start

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            url = "http://localhost:8000"
            print(f"Navigating to {url}")
            page.goto(url)

            # Verify initial state
            counter = page.locator("#counter")
            expect(counter).to_have_text("Cookies Baked: 0")
            print("Initial counter state verified: 0")

            # Click the cookie 5 times
            cookie = page.locator("#cookie")
            for i in range(5):
                cookie.click()

            expect(counter).to_have_text("Cookies Baked: 5")
            print("Counter after 5 clicks: 5")

            # Reload the page
            print("Reloading page...")
            page.reload()

            # Verify persistence
            counter = page.locator("#counter")
            # This is expected to FAIL before the fix
            try:
                expect(counter).to_have_text("Cookies Baked: 5", timeout=5000)
                print("Persistence verified: Counter is still 5")
            except Exception as e:
                print(f"Persistence check FAILED: {e}")
                raise e

            browser.close()
    finally:
        server_process.terminate()
        server_process.wait()

if __name__ == "__main__":
    test_persistence()
