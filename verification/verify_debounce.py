import os
import time
import subprocess
from playwright.sync_api import sync_playwright

def test_debounce():
    server_process = subprocess.Popen(["python3", "-m", "http.server", "8001"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("http://localhost:8001")

            page.evaluate("""
                window.cookieWrites = 0;
                const originalCookieDescriptor = Object.getOwnPropertyDescriptor(Document.prototype, 'cookie');
                Object.defineProperty(document, 'cookie', {
                    set: function(val) {
                        window.cookieWrites++;
                        return originalCookieDescriptor.set.call(document, val);
                    },
                    configurable: true
                });
            """)

            cookie = page.locator("#cookie")
            for _ in range(10):
                cookie.click()
                time.sleep(0.1) # Rapid clicking (faster than 1s debounce)

            writes_immediate = page.evaluate("window.cookieWrites")
            print(f"Cookie writes immediately after 10 rapid clicks: {writes_immediate}")

            print("Waiting for debounce...")
            time.sleep(1.5)

            writes_after_debounce = page.evaluate("window.cookieWrites")
            print(f"Cookie writes after debounce: {writes_after_debounce}")

            if writes_after_debounce > writes_immediate:
                print("Debounce VERIFIED: Cookie was written after delay.")
            else:
                print("Debounce FAILED: Cookie was not written after delay.")

            browser.close()
    finally:
        server_process.terminate()
        server_process.wait()

if __name__ == "__main__":
    test_debounce()
