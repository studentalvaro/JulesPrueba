# Bolt's Journal - Critical Learnings

## 2026-04-19 - Initial Assessment
**Learning:** Found that the application currently writes to cookies on every single click. In a clicker game, this can be a significant bottleneck during rapid clicking sessions. Cookie writes involve expensive stringification and DOM/IO operations.
**Action:** Plan to implement debouncing for state persistence to ensure we only write to the cookie after a period of inactivity or when the user leaves the page.
