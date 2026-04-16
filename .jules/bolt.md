
## 2026-04-15 - Optimization: Pending List Pattern
**Learning:** In high-frequency event handlers (like click listeners), iterating over a static configuration list to update UI states (e.g., achievements) creates O(N) overhead including redundant DOM lookups and class manipulations.
**Action:** Use a "pending list" pattern. Initialize a list with only the items that need processing. As items reach their target state, remove them from the list. If the list is empty, the handler can return early (O(1)), bypassing all logic. Combine this with DOM element caching for maximum efficiency.
