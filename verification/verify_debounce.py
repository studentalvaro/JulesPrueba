import os
import time
import subprocess
from playwright.sync_api import sync_playwright, expect

def test_debounce():
    server_process = subprocess.Popen(["python3", "-m", "http.server", "8001"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            url = "http://localhost:8001"
            page.goto(url)

            cookie = page.locator("#cookie")
            # Click 10 times quickly
            for i in range(10):
                cookie.click()

            print("Clicked 10 times. Checking cookies immediately (should NOT be saved yet or saved only once if delayed)...")
            cookies = page.context.cookies()
            state_cookie = next((c for c in cookies if c['name'] == '_ab_state'), None)

            # Since the first click might have triggered a setTimeout that hasn't fired yet,
            # and successive clicks reset it, the cookie shouldn't be there yet if we are fast enough.
            # But Playwright click takes some time.

            print(f"Cookie found immediately: {state_cookie is not None}")

            # Wait for debounce (1s + margin)
            print("Waiting 1.5s for debounce...")
            time.sleep(1.5)

            cookies = page.context.cookies()
            state_cookie = next((c for c in cookies if c['name'] == '_ab_state'), None)
            print(f"Cookie found after wait: {state_cookie is not None}")

            if state_cookie:
                import base64, json
                encoded = state_cookie['value']
                data = json.loads(base64.b64decode(encoded).decode())
                print(f"Cookie value: {data['v']}")
                if data['v'] == 10:
                    print("SUCCESS: State correctly persisted after debounce.")
                else:
                    print(f"FAILURE: Expected 10, got {data['v']}")
            else:
                print("FAILURE: Cookie not found after debounce.")

            browser.close()
    finally:
        server_process.terminate()
        server_process.wait()

if __name__ == "__main__":
    test_debounce()
