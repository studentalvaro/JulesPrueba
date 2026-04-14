## 2024-05-23 - [Optimized achievement tracking and DOM access]
**Learning:** In interactive applications with high-frequency events (like a clicker game), O(N) DOM lookups and class manipulations in the hot path can lead to jank. Caching DOM elements and filtering out already-processed items (achievements) ensures the event handler remains O(1) or O(remaining_items) without hitting the DOM unnecessarily.
**Action:** Always cache DOM elements used in frequent event handlers and maintain a list of 'pending' work to minimize redundant checks.
