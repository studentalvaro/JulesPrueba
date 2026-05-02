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

            # Monkey patch cookie setter to track writes
            page.evaluate("""
                window.cookieWrites = 0;
                const originalDescriptor = Object.getOwnPropertyDescriptor(Document.prototype, 'cookie');
                Object.defineProperty(document, 'cookie', {
                    set: function(val) {
                        window.cookieWrites++;
                        originalDescriptor.set.call(this, val);
                    },
                    get: function() {
                        return originalDescriptor.get.call(this);
                    },
                    configurable: true
                });
            """)

            cookie = page.locator("#cookie")
            # Rapid clicks (should be debounced)
            for _ in range(10):
                cookie.click()
                time.sleep(0.1)

            writes_mid = page.evaluate("window.cookieWrites")
            print(f"Cookie writes during rapid clicking: {writes_mid}")

            # Wait for debounce
            time.sleep(1.5)
            writes_after = page.evaluate("window.cookieWrites")
            print(f"Cookie writes after waiting for debounce: {writes_after}")

            if writes_after > writes_mid:
                print("Debounce working: cookie written after pause.")
            else:
                print("Debounce error: cookie not written after pause.")
                exit(1)

            # Verify reload works with debounced value
            page.reload()
            counter = page.locator("#counter")
            expect(counter).to_have_text("Cookies Baked: 10")
            print("Persistence after debounce verified.")

            browser.close()
    finally:
        server_process.terminate()
        server_process.wait()

if __name__ == "__main__":
    verify_debounce()
