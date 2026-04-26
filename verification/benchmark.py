import asyncio
import time
from playwright.async_api import async_playwright

async def run_benchmark():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()

        # Start a local server to handle cookies properly
        import subprocess
        server = subprocess.Popen(['python3', '-m', 'http.server', '8001'])
        await asyncio.sleep(1)

        await page.goto('http://localhost:8001/index.html')

        cookie = await page.wait_for_selector('#cookie')

        start_time = time.time()
        for _ in range(100):
            await cookie.click()
        end_time = time.time()

        duration = end_time - start_time
        print(f"Time for 100 clicks: {duration:.4f} seconds")
        print(f"Average time per click: {(duration/100)*1000:.4f} ms")

        server.terminate()
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_benchmark())
