import time
import subprocess
from playwright.sync_api import sync_playwright

def run_benchmark():
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

            start_time = time.time()
            num_clicks = 100
            for i in range(num_clicks):
                cookie.click()
            end_time = time.time()

            total_time = end_time - start_time
            avg_time = (total_time / num_clicks) * 1000

            print(f"Total time for {num_clicks} clicks: {total_time:.4f}s")
            print(f"Average time per click: {avg_time:.2f}ms")

            browser.close()
    finally:
        server_process.terminate()
        server_process.wait()

if __name__ == "__main__":
    run_benchmark()
