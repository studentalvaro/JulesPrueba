## 2024-04-22 - Debounce Cookie Persistence
**Learning:** In high-frequency interaction applications (like clickers), performing expensive operations (JSON stringification, integrity hashing, and cookie writes) on every event significantly bottlenecks the main thread and can lead to perceived lag or frame drops. Debouncing these operations minimizes CPU and I/O overhead while maintaining state consistency.
**Action:** Always consider debouncing or throttling persistence logic for frequently updated state. Use 'beforeunload' listeners to ensure final state is captured.
