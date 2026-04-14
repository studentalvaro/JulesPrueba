document.addEventListener('DOMContentLoaded', () => {
    // Helper functions for cookies
    function setCookie(name, value, days) {
        let expires = "";
        if (days) {
            const date = new Date();
            date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
            expires = "; expires=" + date.toUTCString();
        }
        document.cookie = name + "=" + (value || "") + expires + "; path=/";
    }

    function getCookie(name) {
        const nameEQ = name + "=";
        const ca = document.cookie.split(';');
        for (let i = 0; i < ca.length; i++) {
            let c = ca[i];
            while (c.charAt(0) == ' ') c = c.substring(1, c.length);
            if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
        }
        return null;
    }

    // Load initial count from cookie or default to 0
    let count = parseInt(getCookie('cookie_clicks')) || 0;

    const cookie = document.getElementById('cookie');
    const counterDisplay = document.getElementById('counter');

    // Update display with initial count
    if (counterDisplay) {
        counterDisplay.textContent = `Cookies Baked: ${count}`;
    }

    if (cookie && counterDisplay) {
        cookie.addEventListener('click', () => {
            count++;
            counterDisplay.textContent = `Cookies Baked: ${count}`;
            
            // Save count to cookie (expires in 30 days)
            setCookie('cookie_clicks', count, 30);

            // Micro-animation for the cookie
            cookie.style.transform = 'scale(0.95)';
            setTimeout(() => {
                cookie.style.transform = 'scale(1)';
            }, 100);

            // Creative feedback: Sparkle or particle effect could go here
            console.log(`Baking cookie #${count}...`);
        });
    }
});
