# Bolt's Journal - Critical Learnings

## 2025-05-14 - Initial Profiling
**Learning:** Synchronous cookie writes and repeated DOM lookups in a high-frequency click handler create a measurable bottleneck (26s for 100 clicks in Playwright).
**Action:** Always debounce persistence and cache DOM elements for high-frequency interactive elements.
