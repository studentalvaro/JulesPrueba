## 2024-05-22 - Optimizing high-frequency click handler

**Learning:** In a clicker-style application, every click triggers a cascade of side effects: DOM updates, achievement checks, and state persistence. Synchronous cookie writes and repeated DOM lookups are significant bottlenecks when scaled. In this app, 100 clicks were performing 100 cookie writes (with integrity hash generation) and over 300 DOM lookups.

**Action:**
1. Cache all frequently accessed DOM elements outside the event loop.
2. Implement debouncing for state persistence (I/O and heavy computation) during bursts of activity.
3. Use the `visibilitychange` event as a fallback to ensure final state persistence when the user departs, allowing for aggressive debouncing during active play.
4. Measure impact using targeted scripts that monkeypatch browser APIs (`document.cookie`, `document.getElementById`) to count operations, as raw execution time can be masked by external factors like Playwright's IPC overhead.
