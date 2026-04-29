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

        print("Starting benchmark: 100 clicks...")
        start_time = time.time()
        for _ in range(100):
            cookie.click()
        end_time = time.time()

        duration = end_time - start_time
        print(f"Benchmark completed in {duration:.4f} seconds")

        counter_text = page.locator("#counter").inner_text()
        print(f"Final state: {counter_text}")

        browser.close()
        return duration

if __name__ == "__main__":
    run_benchmark()
