import os
import time
from playwright.sync_api import sync_playwright

def run_internal_benchmark():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        current_dir = os.path.dirname(os.path.abspath(__file__))
        app_dir = os.path.dirname(current_dir)
        index_path = os.path.join(app_dir, "index.html")
        file_url = f"file://{index_path}"

        # Inject a bypass for isTrusted before the script runs
        page.add_init_script("""
            const originalAddEventListener = EventTarget.prototype.addEventListener;
            EventTarget.prototype.addEventListener = function(type, listener, options) {
                if (type === 'click') {
                    const wrappedListener = function(event) {
                        // Create a proxy to bypass isTrusted check
                        const proxyEvent = new Proxy(event, {
                            get: function(target, prop) {
                                if (prop === 'isTrusted') return true;
                                return target[prop];
                            }
                        });
                        return listener.call(this, proxyEvent);
                    };
                    return originalAddEventListener.call(this, type, wrappedListener, options);
                }
                return originalAddEventListener.call(this, type, listener, options);
            };
        """)

        page.goto(file_url)

        # Confirm the counter starts at 0
        initial_counter = page.locator("#counter").inner_text()
        print(f"Initial: {initial_counter}")

        result = page.evaluate("""() => {
            const cookie = document.getElementById('cookie');
            const start = performance.now();
            for (let i = 0; i < 100; i++) {
                cookie.dispatchEvent(new MouseEvent('click', {
                    view: window,
                    bubbles: true,
                    cancelable: true
                }));
            }
            const end = performance.now();
            return end - start;
        }""")

        print(f"Total time for 100 internal clicks: {result:.4f} ms")
        print(f"Average time per internal click: {result/100:.4f} ms")

        counter_text = page.locator("#counter").inner_text()
        print(f"Counter after internal clicks: {counter_text}")

        browser.close()

if __name__ == "__main__":
    run_internal_benchmark()
