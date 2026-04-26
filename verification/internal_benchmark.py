import time
import subprocess
from playwright.sync_api import sync_playwright

def internal_benchmark():
    server_process = subprocess.Popen(["python3", "-m", "http.server", "8005"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("http://localhost:8005")

            # Measure 1000 simulated clicks via JS
            js_code = """
            (function() {
                const cookie = document.getElementById('cookie');
                const start = performance.now();
                for(let i=0; i<1000; i++) {
                    cookie.click();
                }
                const end = performance.now();
                return end - start;
            })()
            """
            duration = page.evaluate(js_code)
            print(f"Time for 1000 JS clicks: {duration:.2f}ms")
            print(f"Average time per JS click: {duration/1000:.4f}ms")

            browser.close()
    finally:
        server_process.terminate()
        server_process.wait()

if __name__ == '__main__':
    internal_benchmark()
