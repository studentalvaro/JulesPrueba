## 2026-05-06 - Bottleneck in High-Frequency Persistence

**Learning:** High-frequency interactions (like rapid clicking) coupled with synchronous persistence (like `document.cookie` writes) create a severe performance bottleneck. In this application, 100 clicks triggered 100 cookie writes and over 300 DOM lookups, significantly increasing latency and blocking the main thread. Synchronous cookie writes are particularly expensive as they involve I/O.

**Action:** Always implement debouncing or throttling for persistence logic triggered by frequent user events. Use DOM element caching during initialization for any elements accessed within high-frequency event handlers. Additionally, use the `visibilitychange` event to ensure the final state is persisted immediately when the user backgrounds the application, mitigating the risk of data loss from debouncing.
