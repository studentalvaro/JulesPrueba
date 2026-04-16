(function() {
    'use strict';

    document.addEventListener('DOMContentLoaded', () => {
        // --- Security Configuration ---
        const SECRET_SALT = "alvaro_secret_bakery_2024";
        const STORAGE_KEY = "_ab_state";

        // --- Achievements Configuration ---
        const ACHIEVEMENTS = [
            { id: 'ach-10', threshold: 10, name: 'Rookie' },
            { id: 'ach-50', threshold: 50, name: 'Apprentice' },
            { id: 'ach-100', threshold: 100, name: 'Master Baker' }
        ];

        // --- Utils ---

        /**
         * Simple debounce to limit execution frequency of expensive operations.
         */
        function debounce(func, wait) {
            let timeout;
            return function(...args) {
                clearTimeout(timeout);
                timeout = setTimeout(() => func.apply(this, args), wait);
            };
        }

        // --- Anti-Tamper Logic ---

        function generateIntegrityHash(value) {
            let str = value + SECRET_SALT;
            let hash = 0;
            for (let i = 0; i < str.length; i++) {
                hash = ((hash << 5) - hash) + str.charCodeAt(i);
                hash |= 0;
            }
            return btoa(hash.toString());
        }

        const saveSecureState = debounce((count) => {
            const data = {
                v: count,
                h: generateIntegrityHash(count)
            };
            const encoded = btoa(JSON.stringify(data));
            document.cookie = `${STORAGE_KEY}=${encoded}; expires=Fri, 31 Dec 9999 23:59:59 GMT; path=/; SameSite=Strict`;
        }, 500);

        function loadSecureState() {
            const cookies = document.cookie.split('; ');
            const stateCookie = cookies.find(row => row.startsWith(STORAGE_KEY + '='));
            
            if (!stateCookie) return 0;

            try {
                const encoded = stateCookie.split('=')[1];
                const data = JSON.parse(atob(encoded));
                
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

        // --- Core Application Logic ---

        let count = loadSecureState();
        const cookieElement = document.getElementById('cookie');
        const counterDisplay = document.getElementById('counter');

        // Cache achievement elements and track pending ones to avoid O(N) DOM lookups
        const achievementState = ACHIEVEMENTS.map(ach => ({
            ...ach,
            element: document.getElementById(ach.id)
        }));

        let pendingAchievements = achievementState.filter(ach => count < ach.threshold);

        // Initialize unlocked achievements
        achievementState.forEach(ach => {
            if (ach.element && count >= ach.threshold) {
                ach.element.classList.remove('locked');
                ach.element.classList.add('unlocked');
            }
        });

        /**
         * Optimized achievement check: only iterates over pending achievements.
         * Reduces computation from O(N_total) to O(N_pending).
         */
        function updateAchievements() {
            if (pendingAchievements.length === 0) return;

            pendingAchievements = pendingAchievements.filter(ach => {
                if (count >= ach.threshold) {
                    if (ach.element) {
                        ach.element.classList.remove('locked');
                        ach.element.classList.add('unlocked');
                        console.log(`%c✨ Achievement Unlocked: ${ach.name}`, "color: #ffd700; font-weight: bold;");
                    }
                    return false; // Remove from pending
                }
                return true;
            });
        }

        if (counterDisplay) {
            counterDisplay.textContent = `Cookies Baked: ${count}`;
        }
        updateAchievements();

        if (cookieElement && counterDisplay) {
            cookieElement.addEventListener('click', (e) => {
                if (e.isTrusted) {
                    count++;
                    counterDisplay.textContent = `Cookies Baked: ${count}`;
                    saveSecureState(count);
                    updateAchievements();

                    // Micro-animation
                    cookieElement.style.transform = 'scale(0.95)';
                    setTimeout(() => {
                        cookieElement.style.transform = 'scale(1)';
                    }, 100);
                }
            });
        }

        // --- DevTools Protection ---

        document.addEventListener('contextmenu', e => e.preventDefault());
        document.addEventListener('keydown', (e) => {
            if (e.keyCode === 123) { e.preventDefault(); return false; }
            if (e.ctrlKey && e.shiftKey && (e.keyCode === 73 || e.keyCode === 74 || e.keyCode === 67)) {
                e.preventDefault();
                return false;
            }
            if (e.ctrlKey && e.keyCode === 85) { e.preventDefault(); return false; }
        });

        console.log("%cAlvaro's Bakery Security & Achievements Active", "color: #5c4033; font-weight: bold; font-size: 14px;");
    });
})();
