document.addEventListener('DOMContentLoaded', () => {
    let count = 0;
    const cookie = document.getElementById('cookie');
    const counterDisplay = document.getElementById('counter');

    if (cookie && counterDisplay) {
        cookie.addEventListener('click', () => {
            count++;
            counterDisplay.textContent = `Cookies Baked: ${count}`;
            
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
