import time
from playwright.sync_api import sync_playwright
import os
import subprocess
import signal

def run_benchmark():
    # Start a local server
    server_process = subprocess.Popen(["python3", "-m", "http.server", "8000"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)  # Give the server time to start

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto("http://localhost:8000")

            cookie = page.locator("#cookie")

            # Warm up
            for _ in range(10):
                cookie.click()

            iterations = 100
            start_time = time.time()
            for _ in range(iterations):
                cookie.click()
            end_time = time.time()

            duration = end_time - start_time
            print(f"Total time for {iterations} clicks: {duration:.4f} seconds")
            print(f"Average time per click: {(duration/iterations)*1000:.4f} ms")

            browser.close()
    finally:
        os.kill(server_process.pid, signal.SIGTERM)

if __name__ == "__main__":
    run_benchmark()
