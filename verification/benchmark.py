import time
import subprocess
from playwright.sync_api import sync_playwright

def benchmark():
    server_process = subprocess.Popen(["python3", "-m", "http.server", "8000"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("http://localhost:8000")

            cookie = page.locator("#cookie")

            start_time = time.time()
            iterations = 100
            for _ in range(iterations):
                cookie.click()
            end_time = time.time()

            duration = end_time - start_time
            print(f"Time for {iterations} clicks: {duration:.4f}s")
            print(f"Average time per click: {(duration/iterations)*1000:.4f}ms")

            browser.close()
    finally:
        server_process.terminate()
        server_process.wait()

if __name__ == "__main__":
    benchmark()
