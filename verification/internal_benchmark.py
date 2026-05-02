import time
import subprocess
from playwright.sync_api import sync_playwright

def internal_benchmark():
    # Start a local HTTP server
    server_process = subprocess.Popen(["python3", "-m", "http.server", "8005"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)  # Wait for server to start

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            url = "http://localhost:8005"
            page.goto(url)

            # Benchmark internal execution time
            # We bypass e.isTrusted by creating a CustomEvent or just calling the handler logic if we can
            # Actually, we can just measure how long it takes to run the handler logic via page.evaluate

            benchmark_js = """
            () => {
                const cookie = document.getElementById('cookie');
                const start = performance.now();
                for (let i = 0; i < 100; i++) {
                    cookie.dispatchEvent(new MouseEvent('click', {
                        bubbles: true,
                        cancelable: true,
                        view: window
                    }));
                }
                const end = performance.now();
                return end - start;
            }
            """
            # But the current code has if(e.isTrusted).
            # So dispatchEvent won't trigger the count increment.
            # I'll modify the script temporarily for benchmarking or use a different approach.

            # Let's just measure the stats again but with a focus on 'time'

            print("Internal JS execution for 100 clicks (simulated via Playwright clicks):")
            start = time.time()
            for _ in range(100):
                 page.evaluate("document.getElementById('cookie').click()")
            end = time.time()
            print(f"Total time for 100 internal clicks: {(end - start) * 1000:.2f} ms")

            browser.close()
    finally:
        server_process.terminate()
        server_process.wait()

if __name__ == "__main__":
    internal_benchmark()
