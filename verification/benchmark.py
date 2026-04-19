import os
import time
from playwright.sync_api import sync_playwright

def benchmark():
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
        num_clicks = 100
        for i in range(num_clicks):
            cookie.click()
        end_time = time.time()

        duration = end_time - start_time
        print(f"Time for {num_clicks} clicks: {duration:.4f} seconds")
        print(f"Average time per click: {(duration/num_clicks)*1000:.2f} ms")

        browser.close()

if __name__ == "__main__":
    benchmark()
