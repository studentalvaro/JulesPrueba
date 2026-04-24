import time
import subprocess
from playwright.sync_api import sync_playwright

def test_debounce():
    server_process = subprocess.Popen(["python3", "-m", "http.server", "8000"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("http://localhost:8000")

            cookie = page.locator("#cookie")

            # Click 5 times rapidly
            for _ in range(5):
                cookie.click()

            # Check cookies immediately - should be empty or old value (0)
            cookies = page.context.cookies()
            state_cookie = next((c for c in cookies if c['name'] == '_ab_state'), None)

            # Since cookie click is async and we just clicked 5 times,
            # let's wait a tiny bit for the first click to *not* have saved yet.
            # But with 1000ms debounce, it definitely shouldn't be there yet.

            if state_cookie:
                print("Cookie found prematurely (might be from previous session if not cleared)")
            else:
                print("Debounce working: No cookie set immediately after rapid clicks.")

            # Wait for debounce
            print("Waiting for debounce (1.5s)...")
            time.sleep(1.5)

            cookies = page.context.cookies()
            state_cookie = next((c for c in cookies if c['name'] == '_ab_state'), None)
            if state_cookie:
                print("Debounce working: Cookie set after wait.")
            else:
                print("FAILED: Cookie not set after debounce wait.")

            browser.close()
    finally:
        server_process.terminate()
        server_process.wait()

if __name__ == "__main__":
    test_debounce()
