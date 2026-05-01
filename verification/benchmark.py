import time
from playwright.sync_api import sync_playwright
import os
import http.server
import threading

def run_server():
    os.chdir('/app')
    handler = http.server.SimpleHTTPRequestHandler
    httpd = http.server.HTTPServer(('127.0.0.1', 8080), handler)
    httpd.serve_forever()

def benchmark():
    # Start server in a thread
    daemon = threading.Thread(target=run_server, daemon=True)
    daemon.start()
    time.sleep(1) # Wait for server to start

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto('http://127.0.0.1:8080')

        # Warm up
        page.click('#cookie')

        start_time = time.time()
        for _ in range(100):
            page.click('#cookie')
        end_time = time.time()

        total_time = end_time - start_time
        print(f"Total time for 100 clicks: {total_time:.4f}s")
        print(f"Average time per click: {(total_time/100)*1000:.4f}ms")

        browser.close()

if __name__ == "__main__":
    benchmark()
