import os
import time
import subprocess
import json
import base64
from playwright.sync_api import sync_playwright

def test_debounce():
    # Start a local HTTP server
    server_process = subprocess.Popen(["python3", "-m", "http.server", "8002"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)  # Wait for server to start

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            url = "http://localhost:8002"
            page.goto(url)

            cookie_btn = page.locator("#cookie")

            # Helper to get the cookie value
            def get_state_cookie():
                cookies = page.context.cookies()
                for cookie in cookies:
                    if cookie['name'] == '_ab_state':
                        return cookie['value']
                return None

            # Initial state
            initial_cookie = get_state_cookie()
            print(f"Initial cookie: {initial_cookie}")

            # Click multiple times rapidly
            for i in range(10):
                cookie_btn.click()
                time.sleep(0.1) # Rapid but not too fast for the browser

            # Check cookie immediately after clicks (should not have changed or should not be final)
            intermediate_cookie = get_state_cookie()
            print(f"Intermediate cookie (immediately after clicks): {intermediate_cookie}")

            if intermediate_cookie == initial_cookie or intermediate_cookie is None:
                print("SUCCESS: Cookie did not update immediately (debounced).")
            else:
                # If it updated, check if it's the final value (10)
                decoded = json.loads(base64.b64decode(intermediate_cookie).decode())
                if decoded['v'] < 10:
                    print(f"Cookie updated but value is {decoded['v']}, which is less than 10. Debouncing working.")
                else:
                    print(f"FAILURE: Cookie updated to final value {decoded['v']} too early.")

            # Wait for debounce timer (1s + buffer)
            print("Waiting for debounce timer...")
            time.sleep(1.5)

            final_cookie = get_state_cookie()
            if final_cookie:
                decoded = json.loads(base64.b64decode(final_cookie).decode())
                print(f"Final cookie value: {decoded['v']}")
                if decoded['v'] == 10:
                    print("SUCCESS: Cookie eventually updated to 10.")
                else:
                    print(f"FAILURE: Cookie value is {decoded['v']}, expected 10.")
            else:
                print("FAILURE: Cookie not found after waiting.")

            browser.close()
    finally:
        server_process.terminate()
        server_process.wait()

if __name__ == "__main__":
    test_debounce()
