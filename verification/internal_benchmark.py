import os
import time
import subprocess
from playwright.sync_api import sync_playwright

def run_internal_benchmark():
    server_process = subprocess.Popen(["python3", "-m", "http.server", "8002"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("http://localhost:8002")

            # Use page.click to ensure isTrusted=true
            script = """
            async () => {
                const start = performance.now();
                for(let i=0; i<100; i++) {
                    await window.clickCookie();
                }
                const end = performance.now();
                return end - start;
            }
            """

            # We need to expose a way to click from inside or just use playwright's click which is trusted
            # Let's use playwright click in a loop and measure in python, but that includes IPC overhead.

            # Let's try to monkeypatch the click handler to remove isTrusted for benchmarking
            page.evaluate("""
                () => {
                    const cookie = document.getElementById('cookie');
                    // This is hacky but for benchmarking internal logic it works
                    const oldAddEventListener = Element.prototype.addEventListener;
                    Element.prototype.addEventListener = function(type, listener, options) {
                        if (type === 'click' && this.id === 'cookie') {
                            const newListener = (e) => {
                                // Create a fake trusted-like event or just call listener with fake event
                                listener({ ...e, isTrusted: true, preventDefault: () => {}, stopPropagation: () => {} });
                            };
                            oldAddEventListener.call(this, type, newListener, options);
                        } else {
                            oldAddEventListener.call(this, type, listener, options);
                        }
                    };
                }
            """)
            page.reload() # This won't work because reload clears monkeypatch.

            # Alternative: inject script that runs the logic.

            # Let's just measure how long 100 clicks take with page.click()
            start = time.perf_counter()
            for _ in range(100):
                page.click("#cookie")
            end = time.perf_counter()
            print(f"Playwright 100 clicks: {(end-start)*1000:.4f} ms")

            browser.close()
    finally:
        server_process.terminate()
        server_process.wait()

if __name__ == "__main__":
    run_internal_benchmark()
