## 2026-04-29 - Debouncing and DOM Caching
**Learning:** In highly interactive applications like clickers, synchronous cookie writes and repeated DOM lookups in the main event handler create a significant performance bottleneck. For 100 rapid clicks, the internal JS execution time dropped from ~8.5ms to ~3ms by implementing debouncing and caching.
**Action:** Always check for high-frequency events (like clicks or mouse moves) and ensure they don't trigger expensive operations (I/O, heavy computation, DOM lookups) on every fire.
