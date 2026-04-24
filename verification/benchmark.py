import os
import time
import subprocess
from playwright.sync_api import sync_playwright

def run_benchmark():
    # Start a local HTTP server
    server_process = subprocess.Popen(["python3", "-m", "http.server", "8001"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            url = "http://localhost:8001"
            page.goto(url)

            cookie = page.locator("#cookie")

            start_time = time.time()
            for _ in range(100):
                cookie.click()
            end_time = time.time()

            duration = end_time - start_time
            print(f"Benchmark: 100 clicks took {duration:.4f} seconds")

            # Wait a bit to ensure debounced save would have triggered (if I had implemented it)
            time.sleep(1.5)

            browser.close()
            return duration
    finally:
        server_process.terminate()
        server_process.wait()

if __name__ == "__main__":
    run_benchmark()
