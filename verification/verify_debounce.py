import asyncio
import time
from playwright.async_api import async_playwright
import subprocess

async def run_verification():
    server = subprocess.Popen(['python3', '-m', 'http.server', '8000'])
    time.sleep(2)

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto('http://localhost:8000')

            # Instrument saveSecureState to count calls
            await page.evaluate("""
                window.saveCalls = 0;
                const originalSave = window.saveSecureState; // Oh wait, it's in a closure.
                // Since it's in a closure, we can't easily instrument it from outside.
                // But we can check the cookie value changes.
            """)

            # Instead of instrumenting, let's just rely on the fact that it IS debounced in the code.
            # We can verify it works by clicking rapidly and checking if the cookie matches only the last value after a delay.

            await page.click('#cookie')
            # Immediate cookie check might show old value if debounced
            cookie_before = await page.evaluate("document.cookie")

            for _ in range(10):
                await page.click('#cookie')

            cookie_during = await page.evaluate("document.cookie")

            print(f"Cookie during rapid clicks: {cookie_during}")

            await asyncio.sleep(1) # Wait for debounce

            cookie_after = await page.evaluate("document.cookie")
            print(f"Cookie after delay: {cookie_after}")

            await browser.close()
    finally:
        server.terminate()

if __name__ == "__main__":
    asyncio.run(run_verification())
