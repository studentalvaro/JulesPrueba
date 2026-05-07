import os
from playwright.sync_api import sync_playwright

def run_internal_benchmark():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        current_dir = os.path.dirname(os.path.abspath(__file__))
        app_dir = os.path.dirname(current_dir)
        index_path = os.path.join(app_dir, "index.html")
        file_url = f"file://{index_path}"

        # We use add_init_script to ensure it runs before any other script
        page.add_init_script("""
            window.totalHandlerTime = 0;
            const originalAddEventListener = EventTarget.prototype.addEventListener;
            EventTarget.prototype.addEventListener = function(type, listener, options) {
                if (type === 'click' && this.id === 'cookie') {
                    const trackedListener = function(e) {
                        const start = performance.now();
                        listener.call(this, e);
                        const end = performance.now();
                        window.totalHandlerTime += (end - start);
                    };
                    return originalAddEventListener.call(this, type, trackedListener, options);
                }
                return originalAddEventListener.call(this, type, listener, options);
            };
        """)

        page.goto(file_url)

        cookie = page.locator("#cookie")
        for _ in range(100):
            cookie.click()

        total_time = page.evaluate("window.totalHandlerTime")
        if total_time is not None:
            print(f"Total internal JS execution time for 100 clicks: {total_time:.4f} ms")
            print(f"Average internal JS time per click: {total_time / 100:.4f} ms")
        else:
            print("Failed to measure internal time.")

        browser.close()

if __name__ == "__main__":
    run_internal_benchmark()
