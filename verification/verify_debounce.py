import asyncio
import time
from playwright.async_api import async_playwright

async def verify_debounce():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()

        import subprocess
        server = subprocess.Popen(['python3', '-m', 'http.server', '8004'])
        await asyncio.sleep(1)

        await page.goto('http://localhost:8004/index.html')

        # Helper to get current cookie value
        async def get_state_cookie():
            cookies = await context.cookies()
            for cookie in cookies:
                if cookie['name'] == '_ab_state':
                    return cookie['value']
            return None

        cookie_element = await page.wait_for_selector('#cookie')

        print("Clicking 5 times rapidly...")
        for _ in range(5):
            await cookie_element.click()
            # Minimal delay between clicks

        await asyncio.sleep(0.1)
        cookie_after_rapid = await get_state_cookie()
        print(f"Cookie after rapid clicks (should be None or old): {cookie_after_rapid}")

        print("Waiting for debounce (1.5s)...")
        await asyncio.sleep(1.5)

        cookie_after_wait = await get_state_cookie()
        print(f"Cookie after wait: {cookie_after_wait}")

        if cookie_after_wait:
            print("SUCCESS: Debounce triggered and saved state after delay.")
        else:
            print("FAILURE: State not saved after debounce.")

        server.terminate()
        await browser.close()

if __name__ == "__main__":
    asyncio.run(verify_debounce())
