import asyncio
import time
from playwright.async_api import async_playwright
import subprocess

async def run_benchmark():
    server = subprocess.Popen(['python3', '-m', 'http.server', '8000'])
    time.sleep(2)

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto('http://localhost:8000')

            # Inject profiling code
            await page.evaluate("""
                window.clickDurations = [];
                const cookie = document.getElementById('cookie');
                const counter = document.getElementById('counter');

                // We'll wrap the click listener by intercepting it or just trigger it manually
                // Since it's an anonymous listener in a closure, we can't easily wrap it.
                // But we can measure the total time of a click() call.
            """)

            iterations = 500
            start_time = time.time()
            for _ in range(iterations):
                await page.click('#cookie')
            end_time = time.time()

            total_duration = end_time - start_time
            print(f"Total time for {iterations} clicks: {total_duration:.4f}s")
            print(f"Average time per click (including Playwright overhead): {(total_duration/iterations)*1000:.4f}ms")

            # Let's try to measure the execution time of the script logic only
            logic_time = await page.evaluate(f"""
                (async () => {{
                    const cookie = document.getElementById('cookie');
                    const start = performance.now();
                    for(let i=0; i<{iterations}; i++) {{
                        cookie.dispatchEvent(new MouseEvent('click', {{ bubbles: true, cancelable: true, view: window, detail: 1, screenX: 0, screenY: 0, clientX: 0, clientY: 0, ctrlKey: false, altKey: false, shiftKey: false, metaKey: false, button: 0, relatedTarget: null }}));
                    }}
                    const end = performance.now();
                    return end - start;
                }})()
            """)
            print(f"In-browser execution time for {iterations} clicks: {logic_time:.4f}ms")
            print(f"Average in-browser time per click: {logic_time/iterations:.4f}ms")

            await browser.close()
    finally:
        server.terminate()

if __name__ == "__main__":
    asyncio.run(run_benchmark())
