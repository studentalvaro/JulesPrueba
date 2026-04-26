# Bolt Journal - Performance Learnings

## 2024-04-26 - Initial Performance Audit
**Learning:** Synchronous cookie writes and integrity hash generation on every click create a performance bottleneck, especially during rapid interaction. DOM lookups for achievements on every click also add unnecessary overhead.
**Action:** Implement debouncing for state persistence and cache DOM elements for achievements to improve click responsiveness.
