## 2025-05-15 - Debouncing Persistence & DOM Caching
**Learning:** Frequent I/O operations (like writing to `document.cookie`) and redundant DOM lookups in high-frequency event handlers (like click events) create significant performance bottlenecks. In a browser environment, synchronous cookie writes are particularly expensive.
**Action:** Always implement debouncing for persistence logic triggered by frequent user actions. Cache DOM elements during initialization if they are accessed repeatedly in performance-critical paths.
