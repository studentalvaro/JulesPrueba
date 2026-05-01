import time
from playwright.sync_api import sync_playwright
import os
import http.server
import threading
import json
import base64

def run_server():
    os.chdir('/app')
    handler = http.server.SimpleHTTPRequestHandler
    httpd = http.server.HTTPServer(('127.0.0.1', 8081), handler)
    httpd.serve_forever()

def verify_debounce():
    # Start server in a thread
    daemon = threading.Thread(target=run_server, daemon=True)
    daemon.start()
    time.sleep(1)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()
        page.goto('http://127.0.0.1:8081')

        # 1. Initial state
        cookies = context.cookies()
        state_cookie = next((c for c in cookies if c['name'] == '_ab_state'), None)
        assert state_cookie is None or json.loads(base64.b64decode(state_cookie['value']).decode())['v'] == 0

        # 2. Click once
        page.click('#cookie')

        # 3. Check immediately - should not be saved yet due to 1000ms debounce
        time.sleep(0.1)
        cookies = context.cookies()
        state_cookie = next((c for c in cookies if c['name'] == '_ab_state'), None)
        if state_cookie:
            val = json.loads(base64.b64decode(state_cookie['value']).decode())['v']
            assert val == 0, f"Expected cookie to be 0 immediately after click, but got {val}"
        print("✅ Immediate check passed (debounce working)")

        # 4. Wait for debounce to expire
        time.sleep(1.2)
        cookies = context.cookies()
        state_cookie = next((c for c in cookies if c['name'] == '_ab_state'), None)
        assert state_cookie is not None, "Cookie should have been saved after debounce"
        val = json.loads(base64.b64decode(state_cookie['value']).decode())['v']
        assert val == 1, f"Expected cookie to be 1 after debounce, but got {val}"
        print("✅ Delayed check passed (save successful)")

        # 5. Multiple rapid clicks
        for _ in range(5):
            page.click('#cookie')
            time.sleep(0.1)

        # Should still be 1 (last saved value)
        cookies = context.cookies()
        state_cookie = next((c for c in cookies if c['name'] == '_ab_state'), None)
        val = json.loads(base64.b64decode(state_cookie['value']).decode())['v']
        assert val == 1, f"Expected cookie to still be 1 during rapid clicks, but got {val}"
        print("✅ Rapid clicks debounce passed")

        # 6. Wait for final save
        time.sleep(1.2)
        cookies = context.cookies()
        state_cookie = next((c for c in cookies if c['name'] == '_ab_state'), None)
        val = json.loads(base64.b64decode(state_cookie['value']).decode())['v']
        assert val == 6, f"Expected cookie to be 6 after rapid clicks and wait, but got {val}"
        print("✅ Final save passed")

        browser.close()

if __name__ == "__main__":
    try:
        verify_debounce()
        print("ALL DEBOUNCE TESTS PASSED")
    except Exception as e:
        print(f"TEST FAILED: {e}")
        exit(1)
