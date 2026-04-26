import asyncio
import time
from playwright.async_api import async_playwright

async def run_internal_benchmark():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()

        import subprocess
        server = subprocess.Popen(['python3', '-m', 'http.server', '8002'])
        await asyncio.sleep(1)

        await page.goto('http://localhost:8002/index.html')

        # Measure execution time of 100 clicks in the browser context
        execution_time = await page.evaluate("""() => {
            const cookie = document.getElementById('cookie');
            const start = performance.now();
            for (let i = 0; i < 100; i++) {
                cookie.click();
            }
            const end = performance.now();
            return end - start;
        }""")

        print(f"Internal JS execution time for 100 clicks: {execution_time:.4f} ms")
        print(f"Average internal JS time per click: {execution_time/100:.4f} ms")

        server.terminate()
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_internal_benchmark())
