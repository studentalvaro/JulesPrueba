# Bolt's Performance Journal

## 2025-05-14 - Optimizing Click Handler and Persistence
**Learning:** Synchronous cookie writes and integrity hash calculations on every user interaction (like a clicker game) create a significant performance bottleneck. In this application, `document.cookie` writes and `atob`/`JSON.stringify` overhead were measurable even in small batches. Additionally, repeated `document.getElementById` calls for the same elements during high-frequency events add unnecessary DOM traversal overhead.

**Action:** Implement debouncing for persistence logic (especially when using cookies or localStorage) to batch updates. Cache DOM elements during initialization if they are frequently accessed in event handlers. Use `visibilitychange` as a safety net to ensure final state is persisted when debouncing is used.
