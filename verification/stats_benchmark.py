import os
import time
from playwright.sync_api import sync_playwright

def run_stats_benchmark():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Inject stats gathering
        page.add_init_script("""
            window.stats = {
                cookieWrites: 0,
                domLookups: 0,
                handlerStart: 0,
                totalHandlerTime: 0
            };

            // Intercept cookie writes
            const cookieDescriptor = Object.getOwnPropertyDescriptor(Document.prototype, 'cookie');
            Object.defineProperty(document, 'cookie', {
                set: function(v) {
                    window.stats.cookieWrites++;
                    return cookieDescriptor.set.call(this, v);
                },
                get: function() {
                    return cookieDescriptor.get.call(this);
                }
            });

            // Intercept getElementById
            const originalGetElementById = document.getElementById;
            document.getElementById = function(id) {
                window.stats.domLookups++;
                return originalGetElementById.call(this, id);
            };

            // We want to measure the time spent in the click handler.
            // Since we can't easily wrap the anonymous listener, we'll approximate
            // by looking at the execution time of the whole event loop if needed,
            // but let's just stick to counts for now as they are clear bottlenecks.
        """)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        app_dir = os.path.dirname(current_dir)
        index_path = os.path.join(app_dir, "index.html")
        file_url = f"file://{index_path}"

        page.goto(file_url)

        # Click the cookie 100 times using Playwright (trusted events)
        cookie = page.locator("#cookie")
        iterations = 100

        # We also want to measure internal JS time
        # We'll use a trick: measure time between before and after 100 clicks

        print(f"Performing {iterations} clicks...")
        for i in range(iterations):
            cookie.click()

        stats = page.evaluate("window.stats")
        print(f"Results for {iterations} clicks:")
        print(f"Cookie writes: {stats['cookieWrites']}")
        print(f"DOM lookups (getElementById): {stats['domLookups']}")

        browser.close()

if __name__ == "__main__":
    run_stats_benchmark()
