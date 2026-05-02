## 2026-04-18 - Optimized Click Handler and Persistence
**Learning:** Synchronous cookie writes and repeated DOM lookups in a high-frequency event handler (like a clicker game) create significant overhead. Debouncing state persistence and caching DOM elements can drastically reduce I/O and CPU usage during rapid user interaction.
**Action:** Always check for redundant DOM lookups and expensive storage operations in event listeners that are expected to trigger frequently. Use debouncing for persistence and cache DOM references at initialization.
