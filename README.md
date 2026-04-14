# CookieClicker Alvaro

A premium, single-page web application featuring an interactive cookie clicker with persistent score tracking.

## Features

- **Interactive Cookie:** A beautiful, animated cookie that responds to clicks.
- **Persistent Counter:** Your "Cookies Baked" count is saved automatically using browser cookies, so you never lose your progress.
- **Modern UI:** A clean, responsive design built with HTML5, CSS3, and Vanilla JavaScript.
- **Optimized Performance:** Lightweight and fast, with no external dependencies (other than Google Fonts).

## How to Use

1.  Open `index.html` in any modern web browser.
2.  Click on the large cookie 🍪 in "The Interactive Baker" section.
3.  Watch your count grow! Feel free to refresh the page; your progress is safe.

## Technical Details

-   **Persistence:** Uses client-side cookies (`cookie_clicks`) for session-spanning data storage.
-   **Animations:** Smooth CSS transitions and JavaScript-triggered scaling for tactile feedback.
-   **Structure:**
    -   `index.html`: The semantic structure of the application.
    -   `style.css`: Modern, responsive styling with a delicious cookie-themed color palette.
    -   `script.js`: Clean, modular JavaScript handling interactivity and persistence.

## Development & Testing

The project includes automated verification scripts using Playwright:

-   `verification/verify_app.py`: Verifies basic click functionality.
-   `verification/verify_persistence.py`: Verifies that the click count persists after a page reload (requires an HTTP server).

To run verification:
```bash
python3 verification/verify_persistence.py
```
