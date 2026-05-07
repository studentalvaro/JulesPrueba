import os
import time
from playwright.sync_api import sync_playwright

def run_stats_benchmark():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        current_dir = os.path.dirname(os.path.abspath(__file__))
        app_dir = os.path.dirname(current_dir)
        index_path = os.path.join(app_dir, "index.html")
        file_url = f"file://{index_path}"

        page.goto(file_url)

        # Inject script to track cookie writes and getElementById calls
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

            window.domLookups = 0;
            const originalGetElementById = document.getElementById;
            document.getElementById = function(id) {
                window.domLookups++;
                return originalGetElementById.apply(document, [id]);
            };
        """)

        cookie = page.locator("#cookie")
        for _ in range(100):
            cookie.click()

        # Wait for the debounce (1000ms + some buffer)
        time.sleep(1.5)

        stats = page.evaluate("""
            ({
                cookieWrites: window.cookieWrites,
                domLookups: window.domLookups
            })
        """)

        print(f"Stats for 100 clicks (after waiting for debounce):")
        print(f"Cookie writes: {stats['cookieWrites']}")
        print(f"DOM lookups (getElementById): {stats['domLookups']}")

        browser.close()

if __name__ == "__main__":
    run_stats_benchmark()
