import time
import subprocess
from playwright.sync_api import sync_playwright, expect

def verify_debounce():
    # Start a local HTTP server
    server_process = subprocess.Popen(["python3", "-m", "http.server", "8004"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)  # Wait for server to start

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            url = "http://localhost:8004"
            page.goto(url)

            # Click the cookie 5 times rapidly
            cookie = page.locator("#cookie")
            for i in range(5):
                cookie.click()

            # Wait a short time, less than 1000ms
            time.sleep(0.5)

            cookies = page.context.cookies()
            state_cookie = next((c for c in cookies if c['name'] == '_ab_state'), None)

            if state_cookie is None:
                 print("Verified: Cookie NOT set yet (Debounce active)")
            else:
                 print(f"Cookie found early: {state_cookie['value']}")

            # Wait > 1000ms
            time.sleep(1.0)

            cookies = page.context.cookies()
            state_cookie = next((c for c in cookies if c['name'] == '_ab_state'), None)
            if state_cookie is not None:
                import base64, json
                data = json.loads(base64.b64decode(state_cookie['value']))
                print(f"Verified: Cookie set after timeout with value {data['v']}")
            else:
                print("FAILED: Cookie not set after timeout")

            browser.close()
    finally:
        server_process.terminate()
        server_process.wait()

if __name__ == "__main__":
    verify_debounce()
