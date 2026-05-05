import os
import time
import subprocess
from playwright.sync_api import sync_playwright

def run_stats_benchmark():
    server_process = subprocess.Popen(["python3", "-m", "http.server", "8003"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("http://localhost:8003")

            page.evaluate("""
                window.cookieWrites = 0;
                const originalCookie = Object.getOwnPropertyDescriptor(Document.prototype, 'cookie');
                Object.defineProperty(document, 'cookie', {
                    get: function() { return originalCookie.get.call(document); },
                    set: function(val) {
                        window.cookieWrites++;
                        originalCookie.set.call(document, val);
                    }
                });

                window.domLookups = 0;
                const originalGetElementById = document.getElementById;
                document.getElementById = function(id) {
                    window.domLookups++;
                    return originalGetElementById.call(document, id);
                };
            """)

            for _ in range(100):
                page.click("#cookie")

            stats = page.evaluate("""
                () => {
                    return {
                        cookieWrites: window.cookieWrites,
                        domLookups: window.domLookups
                    };
                }
            """)
            print(f"Stats for 100 clicks:")
            print(f"  Cookie writes: {stats['cookieWrites']}")
            print(f"  DOM lookups (getElementById): {stats['domLookups']}")

            browser.close()
    finally:
        server_process.terminate()
        server_process.wait()

if __name__ == "__main__":
    run_stats_benchmark()
