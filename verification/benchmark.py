import os
import time
import subprocess
from playwright.sync_api import sync_playwright

def run_benchmark():
    server_process = subprocess.Popen(["python3", "-m", "http.server", "8001"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)

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
            print(f"Time taken for 100 clicks: {duration:.4f} seconds")
            print(f"Average time per click: {(duration/100)*1000:.2f} ms")

            browser.close()
    finally:
        server_process.terminate()
        server_process.wait()

if __name__ == "__main__":
    run_benchmark()
