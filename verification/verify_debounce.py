import os
import time
from playwright.sync_api import sync_playwright

def test_debounce():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        import subprocess
        server = subprocess.Popen(["python3", "-m", "http.server", "8000"])
        time.sleep(1)

        try:
            page = browser.new_page()
            page.goto("http://localhost:8000/index.html")

            context = page.context
            context.clear_cookies()
            page.reload()

            cookie_btn = page.locator("#cookie")

            # Click once
            cookie_btn.click()
            cookies = context.cookies()
            print(f"Click 1, cookies: {len(cookies)}")

            # Wait for debounce
            print("Waiting for debounce...")
            time.sleep(1.5)
            cookies = context.cookies()
            print(f"After 1.5s, cookies: {len(cookies)}")
            if len(cookies) > 0:
                print(f"Cookie value: {cookies[0]['value']}")

            # Click rapidly
            print("Rapid clicking...")
            for i in range(10):
                cookie_btn.click()
                time.sleep(0.1)

            cookies = context.cookies()
            print(f"Immediately after rapid clicks, cookies: {len(cookies)}")
            # The cookie might still have the value from the first click if it hasn't updated yet
            if len(cookies) > 0:
                 import json
                 import base64
                 val = json.loads(base64.b64decode(cookies[0]['value']))['v']
                 print(f"Cookie value (count): {val}")

            print("Waiting for debounce again...")
            time.sleep(1.5)
            cookies = context.cookies()
            if len(cookies) > 0:
                 val = json.loads(base64.b64decode(cookies[0]['value']))['v']
                 print(f"Final cookie value (count): {val}")

        finally:
            server.terminate()
            browser.close()

if __name__ == "__main__":
    test_debounce()
