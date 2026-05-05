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

        page.goto(file_url)

        # Measure time spent in the click handler (roughly)
        # We'll bypass e.isTrusted by calling the handler logic directly if possible,
        # or just measuring page.evaluate speed.

        js_overhead = page.evaluate("""() => {
            const cookie = document.getElementById('cookie');
            const start = performance.now();
            for(let i=0; i<100; i++) {
                cookie.click();
            }
            return performance.now() - start;
        }""")

        print(f"Internal JS execution time for 100 clicks: {js_overhead:.4f} ms")

        browser.close()

if __name__ == "__main__":
    run_internal_benchmark()
