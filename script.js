(function() {
    'use strict';

    document.addEventListener('DOMContentLoaded', () => {
        // --- Security Configuration ---
        const SECRET_SALT = "alvaro_secret_bakery_2024"; // Obfuscation salt
        const STORAGE_KEY = "_ab_state"; // Obscure storage key

        // --- Anti-Tamper Logic ---

        // Simple obfuscation/hash to detect manual cookie editing
        function generateIntegrityHash(value) {
            let str = value + SECRET_SALT;
            let hash = 0;
            for (let i = 0; i < str.length; i++) {
                hash = ((hash << 5) - hash) + str.charCodeAt(i);
                hash |= 0; // Convert to 32bit integer
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

        function loadSecureState() {
            const cookies = document.cookie.split('; ');
            const stateCookie = cookies.find(row => row.startsWith(STORAGE_KEY + '='));
            
            if (!stateCookie) return 0;

            try {
                const encoded = stateCookie.split('=')[1];
                const data = JSON.parse(atob(encoded));
                
                // Verify integrity
                if (data.h === generateIntegrityHash(data.v)) {
                    return parseInt(data.v) || 0;
                } else {
                    console.error("Bakery Security: Tamper detected. Resetting state.");
                    alert("⚠️ Manual tampering detected. The baker only accepts honest work!");
                    return 0;
                }
            } catch (e) {
                return 0;
            }
        }

        // --- Core Application Logic (Encapsulated) ---

        let count = loadSecureState();
        const cookieElement = document.getElementById('cookie');
        const counterDisplay = document.getElementById('counter');

        if (counterDisplay) {
            counterDisplay.textContent = `Cookies Baked: ${count}`;
        }

        if (cookieElement && counterDisplay) {
            cookieElement.addEventListener('click', (e) => {
                // Basic verification to ensure it's a real user click
                if (e.isTrusted) {
                    count++;
                    counterDisplay.textContent = `Cookies Baked: ${count}`;
                    saveSecureState(count);

                    // Micro-animation
                    cookieElement.style.transform = 'scale(0.95)';
                    setTimeout(() => {
                        cookieElement.style.transform = 'scale(1)';
                    }, 100);
                }
            });
        }

        // --- DevTools Protection (Deterrents) ---

        // Disable Right-Click
        document.addEventListener('contextmenu', e => e.preventDefault());

        // Disable common DevTools shortcuts
        document.addEventListener('keydown', (e) => {
            // F12
            if (e.keyCode === 123) {
                e.preventDefault();
                return false;
            }
            // Ctrl+Shift+I, J, C
            if (e.ctrlKey && e.shiftKey && (e.keyCode === 73 || e.keyCode === 74 || e.keyCode === 67)) {
                e.preventDefault();
                return false;
            }
            // Ctrl+U (View Source)
            if (e.ctrlKey && e.keyCode === 85) {
                e.preventDefault();
                return false;
            }
        });

        console.log("%cAlvaro's Bakery Security Active", "color: #5c4033; font-weight: bold; font-size: 14px;");
    });
})();
