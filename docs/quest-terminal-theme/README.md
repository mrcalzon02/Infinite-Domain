# Infinite Domain Quest Terminal

This layer presents FTB Quests as Charles's surviving field-terminal network
rather than as a generic translucent quest book.

## Implemented shell

- Near-black industrial terminal background with restrained amber hazard stripes.
- Phosphor-green primary text, controls, selection borders, and completion state.
- Cyan task headings and dependency-direction signals.
- Amber rewards, warnings, and active pins.
- Red close/delete controls and a reusable `terminal_critical` semantic style.
- Opaque dark panels, text fields, context menus, slots, and scrollbars.
- Green-tinted FTB controls so the existing interaction vocabulary remains legible.
- Semantic theme selectors for `terminal_warning`, `terminal_critical`, and
  `terminal_classified` quest tags.
- Every chapter has a short subtitle, so the chapter list reads as a terminal
  index instead of an unexplained stack of filenames.
- Every chapter has a fixed identity icon. This suppresses FTB Quests' default
  animated fallback, which cycles through the icons of the chapter's quests.
- Rot records use the critical state, Aberrant/Mekanite records use the warning
  state, and Darknet/Draconic records use the classified state.

Theme source:
`kubejs/assets/ftbquests/ftb_quests_theme.txt`

Primary background:
`kubejs/assets/infinite_domain/textures/gui/quests/terminal_background.png`

## Prologue hardware guide

The optional right-hand branch begins after the shared quest-interface lesson.

| Record | Quest ID | Coverage |
|---|---|---|
| Field Quest Hardware | `6F01000000000020` | Network and permission model |
| Task Screens | `6F01000000000021` | 1x1, 3x3, 5x5, and 7x7 displays |
| Task Screen Configurator | `6F01000000000022` | Task binding and safe use |
| Quest Detectors | `6F01000000000023` | Quest state, notifications, and redstone |
| Quest and Stage Barriers | `6F01000000000024` | Controlled access and containment |
| Loot Crate Equipment | `6F01000000000025` | Crate opening and storage |
| Build a Task Screen | `6F01000000000026` | Craft one screen; receive one configurator |

The guide is optional and does not gate Era 0.

## Validation

Run `python scripts/audit_terminal_quest_theme.py` for theme, asset, icon,
localization, quest-placement, and guide-coverage checks. The general FTB Quests
audit remains authoritative for global IDs, dependencies, localization, groups,
and rewarded-checkmark policy.

## Runtime review still required

FTB's theme parser and final GUI scaling operate in the client. After launch,
visually verify:

1. the background fills common aspect ratios without obscuring quest nodes;
2. chapter and quest panels remain opaque and readable at GUI scales 2 through 4;
3. hover, disabled, locked, active, and completed states remain distinct;
4. the Prologue opens on its first quest and the new branch is visible to its right;
5. the Task Screen recipe and configurator reward behave as described;
6. no third-party resource pack with higher priority replaces the terminal theme.
