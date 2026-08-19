# Recipe Load Failure Audit

Generated from `logs/latest.log`. All overrides live in `kubejs/data`; no mod JAR was edited.

## Resolution summary

| Resolution | Count |
|---|---:|
| repaired | 14 |
| suppressed | 78 |

## Failures by namespace

| Namespace | Count |
|---|---:|
| ae2lt | 1 |
| createcybernetics | 47 |
| createoritechcompat | 14 |
| gearbox | 16 |
| mekanite_mobs | 8 |
| powergrid_batteries | 5 |
| wandofvariance | 1 |

## Policy

- Repaired recipes retain their original ingredients and outputs, changing only the obsolete `item` result field to the Minecraft 1.21.1 `id` field.
- Suppressed recipes reference content that is absent, disabled, or never registered. Their IDs are shadowed by a permanently-false NeoForge condition.
- The CSV beside this report records every recipe ID, source JAR, original error, action, and override path.

A fresh game launch is the authoritative validation. The remaining `Parsing error loading recipe` count should fall from 92 to zero.

One additional recipe (`createcybernetics:basalt`) failed during raw JSON loading before RecipeManager counted it. A hand-authored override repairs its truncated condition array, bringing the total repaired/suppressed recipe resources to 93.
