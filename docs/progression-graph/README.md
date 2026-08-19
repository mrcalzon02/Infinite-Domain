# Recipe and Acquisition Graph

This graph merges recipes from every installed mod JAR with Infinite Domain overrides, then adds item acquisition edges from loot tables, FTB Quests item rewards, and configured worldgen block states.

| Measure | Count |
|---|---:|
| Recipe definitions discovered | 21078 |
| Effective recipes graphed | 21000 |
| Deliberately disabled recipes excluded | 78 |
| Graph nodes | 52361 |
| Graph edges | 73403 |
| Potential multi-route bypasses | 7846 |
| Data files that could not be decoded as JSON | 24 |

## Files

- `graph-nodes.csv`: resources, recipes, loot sources, quest sources, and worldgen sources.
- `graph-edges.csv`: directed ingredient, output, loot, quest, and worldgen relationships.
- `bypass-candidates.csv`: resources with multiple acquisition kinds or at least three independent routes.
- `unparsed-data-files.csv`: static-analysis gaps requiring review.

## Interpretation boundary

This is the complete graph of statically declared JSON recipes and the listed acquisition systems in the installed files. Runtime-generated recipes, code-only mob drops or trades, tags expanded only inside the live game, and economy systems stored in proprietary configuration formats still need targeted adapters. A candidate is not automatically a progression bypass; it becomes one when its route is available earlier or more cheaply than the intended era gate.
