import os
from playwright.sync_api import sync_playwright

def run_benchmark():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        current_dir = os.path.dirname(os.path.abspath(__file__))
        app_dir = os.path.dirname(current_dir)
        index_path = os.path.join(app_dir, "index.html")
        file_url = f"file://{index_path}"

        page.goto(file_url)

        # Inject stats tracker
        page.evaluate("""
            window.stats = {
                cookieWrites: 0,
                getElementByIdCalls: 0
            };

            const originalGetElementById = document.getElementById;
            document.getElementById = function(id) {
                window.stats.getElementByIdCalls++;
                return originalGetElementById.apply(document, arguments);
            };

            const originalCookieDescriptor = Object.getOwnPropertyDescriptor(Document.prototype, 'cookie');
            Object.defineProperty(document, 'cookie', {
                get: function() { return originalCookieDescriptor.get.call(document); },
                set: function(val) {
                    window.stats.cookieWrites++;
                    return originalCookieDescriptor.set.call(document, val);
                },
                configurable: true
            });
        """)

        cookie = page.locator("#cookie")
        for _ in range(100):
            cookie.click()

        stats = page.evaluate("window.stats")
        print(f"Stats for 100 clicks:")
        print(f"  Cookie writes: {stats['cookieWrites']}")
        print(f"  getElementById calls: {stats['getElementByIdCalls']}")

        browser.close()

if __name__ == "__main__":
    run_benchmark()
