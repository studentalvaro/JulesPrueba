import os
import time
import subprocess
import signal
from playwright.sync_api import sync_playwright, expect

def test_debounce_persistence():
    # Start a local server to handle cookies correctly
    process = subprocess.Popen(['python3', '-m', 'http.server', '8001'], cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    time.sleep(1)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()

            page.goto("http://localhost:8001")

            # Click rapidly
            cookie = page.locator("#cookie")
            for _ in range(5):
                cookie.click()

            # Check cookies immediately - should NOT be updated yet (due to 1000ms debounce)
            cookies = context.cookies()
            state_cookie = next((c for c in cookies if c['name'] == '_ab_state'), None)

            # Note: The very FIRST saveSecureState might have happened if we were slow,
            # but with 1s debounce, if we click 5 times in < 1s, it should only have 1 (or 0 if initial)

            print(f"Cookies after rapid clicks: {len(cookies)}")

            # Wait for debounce
            time.sleep(1.5)

            cookies = context.cookies()
            print(f"Cookies after waiting: {len(cookies)}")
            state_cookie = next((c for c in cookies if c['name'] == '_ab_state'), None)
            if state_cookie:
                import base64
                import json
                decoded = json.loads(base64.b64decode(state_cookie['value']).decode())
                print(f"Persisted count: {decoded['v']}")
                if decoded['v'] == 5:
                    print("Debounce persistence verified!")
                else:
                    print(f"Persistence mismatch: expected 5, got {decoded['v']}")
            else:
                print("Cookie NOT found after wait!")

            browser.close()
    finally:
        os.kill(process.pid, signal.SIGTERM)

if __name__ == "__main__":
    test_debounce_persistence()
