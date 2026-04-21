# Bolt's Journal - Critical Learnings

## 2025-04-21 - Debouncing Cookie Persistence
**Learning:** In a clicker game, every click triggering a cookie write (which involves hashing and base64 encoding) can significantly impact the main thread's responsiveness and overall click latency. Debouncing these operations can lead to a much smoother user experience.
**Action:** Always consider debouncing expensive persistence operations in high-frequency interaction scenarios, ensuring a `beforeunload` listener is present to prevent data loss.
