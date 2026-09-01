# Ex Deorum Punishing Fallback Audit

Infinite Domain treats Ex Deorum as a desperate fallback resource path, not a primary mining replacement.

- Ordinary and compressed sieve recipes overridden: 1692
- Input/mesh tables with a guaranteed baseline result: 132
- Recipes with probability reduced: 1560
- Probability multiplier: 0.025 (2.5% of upstream chance)
- Generated recipe overrides: `kubejs/data/exdeorum/recipe/sieve` and `compressed_sieve`

Every valid input/mesh table now yields exactly one guaranteed baseline item selected from its most common upstream result. All other results inherit the probability multiplier. Compressed sieve baseline recipes are also capped at one guaranteed item; their bonus recipes retain their upstream trial counts. Server configuration separately disables simultaneous sieve use, imposes a two-second manual interval, slows composting, and sharply increases mechanical FE costs.

Regenerate these overrides whenever the Ex Deorum JAR version changes.
