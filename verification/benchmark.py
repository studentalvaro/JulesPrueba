import os
import time
from playwright.sync_api import sync_playwright

def benchmark_clicks():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        current_dir = os.path.dirname(os.path.abspath(__file__))
        app_dir = os.path.dirname(current_dir)
        index_path = os.path.join(app_dir, "index.html")
        file_url = f"file://{index_path}"

        page.goto(file_url)

        cookie = page.locator("#cookie")

        start_time = time.time()
        for _ in range(100):
            cookie.click()
        end_time = time.time()

        duration = end_time - start_time
        print(f"Time for 100 clicks: {duration:.4f} seconds")
        print(f"Average time per click: {(duration/100)*1000:.2f} ms")

        browser.close()

if __name__ == "__main__":
    benchmark_clicks()
