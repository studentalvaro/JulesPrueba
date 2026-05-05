import os
import time
import subprocess
from playwright.sync_api import sync_playwright

def test_debounce_logic():
    # Start a local HTTP server
    server_process = subprocess.Popen(["python3", "-m", "http.server", "8004"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("http://localhost:8004")

            # Monkeypatch to track cookie writes
            page.evaluate("""
                window.cookieWrites = 0;
                const originalCookie = Object.getOwnPropertyDescriptor(Document.prototype, 'cookie');
                Object.defineProperty(document, 'cookie', {
                    get: function() { return originalCookie.get.call(document); },
                    set: function(val) {
                        if (val.includes('_ab_state=')) {
                            window.cookieWrites++;
                        }
                        originalCookie.set.call(document, val);
                    }
                });
            """)

            # Perform 10 rapid clicks
            cookie = page.locator("#cookie")
            for _ in range(10):
                cookie.click()
                time.sleep(0.05) # Very fast clicks

            # Immediately after clicks, cookieWrites should still be 0 (due to 1000ms debounce)
            writes_after_burst = page.evaluate("window.cookieWrites")
            print(f"Cookie writes immediately after burst: {writes_after_burst}")

            # Wait for debounce to trigger (1000ms + some buffer)
            time.sleep(1.5)

            writes_after_wait = page.evaluate("window.cookieWrites")
            print(f"Cookie writes after waiting for debounce: {writes_after_wait}")

            # It should be 1 if everything happened within 1 second of each other
            if writes_after_wait == 1:
                print("Debounce logic verified successfully!")
            else:
                print(f"Debounce logic verification FAILED. Expected 1 write, got {writes_after_wait}")
                # We don't raise exception here to allow the test to finish, but we check it in the end.

            # Test visibilitychange immediate save
            page.evaluate("window.cookieWrites = 0")
            cookie.click()
            # Trigger visibilitychange
            page.evaluate("document.dispatchEvent(new Event('visibilitychange'))")
            # This doesn't actually change visibilityState, let's try to set it
            page.evaluate("""
                Object.defineProperty(document, 'visibilityState', { value: 'hidden', writable: true });
                document.dispatchEvent(new Event('visibilitychange'));
            """)

            writes_after_visibility = page.evaluate("window.cookieWrites")
            print(f"Cookie writes after visibilitychange: {writes_after_visibility}")

            if writes_after_visibility >= 1:
                print("Visibilitychange immediate save verified!")
            else:
                print("Visibilitychange immediate save FAILED.")

            browser.close()

            if writes_after_wait == 1 and writes_after_visibility >= 1:
                return True
            return False

    finally:
        server_process.terminate()
        server_process.wait()

if __name__ == "__main__":
    success = test_debounce_logic()
    if not success:
        exit(1)
