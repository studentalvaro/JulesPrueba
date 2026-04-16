import asyncio
import time
from playwright.async_api import async_playwright
import os

async def benchmark():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Using file protocol for simplicity in benchmark
        url = f"file://{os.getcwd()}/index.html"
        await page.goto(url)

        # Ensure cookie is loaded and ready
        cookie = page.locator("#cookie")
        await cookie.wait_for()

        print("Starting benchmark: 1000 clicks...")
        start_time = time.time()

        for _ in range(1000):
            await cookie.click()

        end_time = time.time()
        duration = end_time - start_time

        print(f"Benchmark completed in {duration:.4f} seconds")
        print(f"Average time per click: {(duration / 1000) * 1000:.4f} ms")

        await browser.close()
        return duration

if __name__ == "__main__":
    asyncio.run(benchmark())
