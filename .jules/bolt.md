## 2024-04-23 - Persistence and Achievement Optimization
**Learning:** In highly interactive applications like clickers, frequent I/O (like cookie writes) and DOM lookups (like achievement checks) are the primary performance bottlenecks. Debouncing persistence and caching DOM references significantly reduces the overhead per interaction.
**Action:** Always debounce state-saving operations that involve expensive calculations or storage I/O. Cache DOM element references during initialization if they are frequently accessed in event listeners.
