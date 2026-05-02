import time
import subprocess
from playwright.sync_api import sync_playwright

def stats_benchmark():
    # Start a local HTTP server
    server_process = subprocess.Popen(["python3", "-m", "http.server", "8003"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)  # Wait for server to start

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            url = "http://localhost:8003"
            page.goto(url)

            stats_js = """
            () => {
                window.cookieWrites = 0;
                // Monkey patch cookie
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

                window.getElementByIdCalls = 0;
                const originalGetElementById = document.getElementById;
                document.getElementById = function(id) {
                    window.getElementByIdCalls++;
                    return originalGetElementById.call(this, id);
                };
            }
            """
            page.evaluate(stats_js)

            cookie = page.locator("#cookie")
            for _ in range(100):
                cookie.click()

            # Wait a bit in case there's async stuff (though currently there isn't)
            time.sleep(1)

            writes = page.evaluate("window.cookieWrites")
            lookups = page.evaluate("window.getElementByIdCalls")

            print(f"Cookie writes for 100 clicks: {writes}")
            print(f"getElementById calls for 100 clicks: {lookups}")

            browser.close()
    finally:
        server_process.terminate()
        server_process.wait()

if __name__ == "__main__":
    stats_benchmark()
