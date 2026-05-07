import os
import time
from playwright.sync_api import sync_playwright

def verify_debounce():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Start a local server to handle cookies correctly if needed
        # But file:// usually works for simple cases, let's see.
        # Actually verify_persistence.py uses http.server.

        import subprocess
        server_process = subprocess.Popen(["python3", "-m", "http.server", "8001"])
        time.sleep(1)

        try:
            page.goto("http://localhost:8001")

            # Instrument
            page.evaluate("""
                window.cookieWrites = 0;
                const originalCookie = Object.getOwnPropertyDescriptor(Document.prototype, 'cookie');
                Object.defineProperty(document, 'cookie', {
                    set: function(val) {
                        window.cookieWrites++;
                        originalCookie.set.call(this, val);
                    },
                    get: function() {
                        return originalCookie.get.call(this);
                    }
                });
            """)

            cookie = page.locator("#cookie")

            # Click 5 times rapidly
            for _ in range(5):
                cookie.click()

            writes_immediate = page.evaluate("window.cookieWrites")
            print(f"Cookie writes immediately after rapid clicks: {writes_immediate}")

            # Wait for debounce
            time.sleep(1.5)

            writes_after = page.evaluate("window.cookieWrites")
            print(f"Cookie writes after waiting for debounce: {writes_after}")

            if writes_immediate < 5 and writes_after > writes_immediate:
                print("Debounce logic confirmed!")
            else:
                print("Debounce logic NOT working as expected.")

            # Test visibilitychange
            # We can't easily trigger visibilityState 'hidden' in Playwright directly
            # to trigger the listener, but we can dispatch the event.

            page.evaluate("""
                // Reset counter for visibility test
                window.cookieWrites = 0;
            """)

            cookie.click()
            page.evaluate("""
                Object.defineProperty(document, 'visibilityState', { value: 'hidden', writable: true });
                document.dispatchEvent(new Event('visibilitychange'));
            """)

            writes_visibility = page.evaluate("window.cookieWrites")
            print(f"Cookie writes after visibilitychange: {writes_visibility}")

            if writes_visibility == 1:
                print("Visibility persistence confirmed!")
            else:
                print("Visibility persistence NOT confirmed.")

        finally:
            server_process.terminate()
            browser.close()

if __name__ == "__main__":
    verify_debounce()
