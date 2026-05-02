import os
import time
from playwright.sync_api import sync_playwright

def run_benchmark():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Construct the file path to index.html
        current_dir = os.path.dirname(os.path.abspath(__file__))
        app_dir = os.path.dirname(current_dir)
        index_path = os.path.join(app_dir, "index.html")
        file_url = f"file://{index_path}"

        page.goto(file_url)

        cookie = page.locator("#cookie")

        # Warm up
        cookie.click()

        iterations = 100
        start_time = time.time()
        for i in range(iterations):
            cookie.click()
        end_time = time.time()

        duration = end_time - start_time
        print(f"Time for {iterations} clicks: {duration:.4f} seconds")
        print(f"Average time per click: {(duration/iterations)*1000:.4f} ms")

        browser.close()

if __name__ == "__main__":
    run_benchmark()
