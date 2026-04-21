import os
import time
import subprocess
from playwright.sync_api import sync_playwright

def benchmark():
    # Start a local HTTP server
    server_process = subprocess.Popen(["python3", "-m", "http.server", "8001"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)  # Wait for server to start

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            url = "http://localhost:8001"
            page.goto(url)

            cookie = page.locator("#cookie")

            num_clicks = 100
            start_time = time.time()
            for i in range(num_clicks):
                cookie.click()
            end_time = time.time()

            duration = end_time - start_time
            print(f"Total time for {num_clicks} clicks: {duration:.4f}s")
            print(f"Average time per click: {(duration/num_clicks)*1000:.4f}ms")

            browser.close()
    finally:
        server_process.terminate()
        server_process.wait()

if __name__ == "__main__":
    benchmark()
