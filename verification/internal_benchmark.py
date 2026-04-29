import os
import time
from playwright.sync_api import sync_playwright

def run_internal_benchmark():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        current_dir = os.path.dirname(os.path.abspath(__file__))
        app_dir = os.path.dirname(current_dir)
        index_path = os.path.join(app_dir, "index.html")
        file_url = f"file://{index_path}"

        page.goto(file_url)

        # Bypass isTrusted for benchmarking
        page.evaluate("window.BENCHMARKING = true;")

        js_code = """
        () => {
            const cookie = document.getElementById('cookie');
            // We need to trigger the handler manually or bypass the check
            // Let's modify the script temporarily in the page
            const originalAddEventListener = Element.prototype.addEventListener;
            let clickHandler;
            Element.prototype.addEventListener = function(type, listener, options) {
                if (type === 'click' && this.id === 'cookie') {
                    clickHandler = listener;
                }
                return originalAddEventListener.call(this, type, listener, options);
            };

            // Reload or re-run the script? Hard.
            // Alternative: find the handler.
            // Better: evaluate the performance of what IS inside the handler.
        }
        """

        # Let's just measure the saveSecureState and updateAchievements functions
        # We can extract them or just run 100 iterations of what the click handler does

        bench_js = """
        () => {
            // Re-define/Capture what's in the click handler
            // Since it's in an IIFE, we can't easily grab them.
            // But we can simulate the work.

            const SECRET_SALT = "alvaro_secret_bakery_2024";
            const STORAGE_KEY = "_ab_state";
            const ACHIEVEMENTS = [
                { id: 'ach-10', threshold: 10, name: 'Rookie' },
                { id: 'ach-50', threshold: 50, name: 'Apprentice' },
                { id: 'ach-100', threshold: 100, name: 'Master Baker' }
            ];

            function generateIntegrityHash(value) {
                let str = value + SECRET_SALT;
                let hash = 0;
                for (let i = 0; i < str.length; i++) {
                    hash = ((hash << 5) - hash) + str.charCodeAt(i);
                    hash |= 0;
                }
                return btoa(hash.toString());
            }

            function saveSecureState(count) {
                const data = {
                    v: count,
                    h: generateIntegrityHash(count)
                };
                const encoded = btoa(JSON.stringify(data));
                document.cookie = `${STORAGE_KEY}=${encoded}; expires=Fri, 31 Dec 9999 23:59:59 GMT; path=/; SameSite=Strict`;
            }

            function updateAchievements(count) {
                ACHIEVEMENTS.forEach(ach => {
                    const element = document.getElementById(ach.id);
                    if (element) {
                        if (count >= ach.threshold) {
                            if (element.classList.contains('locked')) {
                                element.classList.remove('locked');
                                element.classList.add('unlocked');
                            }
                        } else {
                            element.classList.add('locked');
                            element.classList.remove('unlocked');
                        }
                    }
                });
            }

            const start = performance.now();
            let count = 0;
            for (let i = 0; i < 100; i++) {
                count++;
                // counterDisplay.textContent = `Cookies Baked: ${count}`; // Skip DOM for pure logic bench
                saveSecureState(count);
                updateAchievements(count);
            }
            const end = performance.now();
            return end - start;
        }
        """

        # We use http.server because cookies don't work well with file:// in some contexts
        import subprocess
        import signal

        process = subprocess.Popen(['python3', '-m', 'http.server', '8080'], cwd=app_dir)
        time.sleep(1)

        try:
            page.goto("http://localhost:8080")
            duration = page.evaluate(bench_js)
            print(f"Internal JS time for 100 iterations (including cookie writes): {duration:.4f}ms")
        finally:
            os.kill(process.pid, signal.SIGTERM)

        browser.close()

if __name__ == "__main__":
    run_internal_benchmark()
