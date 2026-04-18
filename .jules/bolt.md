## 2026-04-18 - Debounced Persistence

**Learning:** Synchronous cookie writes and integrity hash generation during rapid user interactions (like in a clicker game) can create unnecessary overhead. While individual calls are fast, the aggregate I/O and CPU usage can be significant in high-frequency scenarios.

**Action:** Always debounce state persistence logic that involves expensive operations (crypto, I/O) in high-frequency event handlers, ensuring a 'beforeunload' listener is present to prevent data loss.
