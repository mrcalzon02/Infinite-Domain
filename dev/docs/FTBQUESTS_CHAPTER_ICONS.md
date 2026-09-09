# FTB Quests chapter icons

## Symptom

The Era chapter buttons — the grand chapter selectors down the side of the quest
book — had no fixed icon. Each one animated through every quest icon in its
chapter. Icons were added repeatedly and were gone again every time the pack was
next loaded.

## Root cause

Not a design mistake and not the game "randomly" dropping them. Every previous
fix wrote the icon in a form FTB Quests cannot read.

`QuestObjectBase.readData` (ftb-quests-neoforge-2101.1.30) does:

```java
this.rawIcon = singleItemOrMissingFromNBT(nbt.getCompound("icon"), provider);
```

and `writeData` does:

```java
if (!rawIcon.isEmpty()) { /* emit "icon" via ItemStack.SINGLE_ITEM_CODEC */ }
```

`CompoundTag.getCompound(key)` returns an **empty compound** when the stored tag
is not a compound. So an icon written as a string:

```
icon: "create:andesite_alloy"          <-- unreadable
```

is a `StringTag`, `getCompound` hands back an empty compound,
`singleItemOrMissingFromNBT` short-circuits on `isEmpty()` and returns
`ItemStack.EMPTY`, and `writeData` then **omits the field entirely** the next time
the quest file is saved. The icon deletes itself.

(`QuestObjectBase.processItemTagData` does contain a `StringTag` branch that would
have handled this — but `readData` never passes a `StringTag` to it, because
`getCompound` filtered it out first. That dead branch is why the string form
*looks* supported.)

With `rawIcon` empty, `getIcon()` falls through to `Chapter.getAltIcon()`:

```java
List<Icon> list = quests.stream().map(Quest::getIcon).toList();
return IconAnimation.fromList(list, false);
```

which is precisely the endless cycling through every icon in the chapter.

The correct form matches `ItemStack.SINGLE_ITEM_CODEC` (`id`, optional
`components`, count implicitly 1):

```
icon: { id: "create:andesite_alloy" }   <-- round-trips
```

The proof was already in the repo: `stellaris_space_industrialization.snbt` was
the only chapter whose icon had ever survived a play session, and it was the only
one written as a compound.

Quest-level icons use the same storage and have the same bug.

## What kept re-breaking it

`dev/scripts/generators/ensure_ftbquest_icons.js` emitted the string form for
both chapter and quest icons, and its first action was to **strip any existing
top-level icon** (`text.replace(/^\ticon:[^\n]*\n/gm, '')`) before rewriting it.
So each run replaced working icons with self-deleting ones. Its git history shows
the cycle plainly: a CI run adds string-form icons, the next commit from the
instance no longer has them, repeat.

## Current layout

| File | Role |
| --- | --- |
| `dev/docs/ftbquests-chapter-icons.json` | **authority.** Per-chapter ordered `candidates` list. |
| `dev/docs/ftbquests-chapter-icons.lock.json` | generated. Resolved chapter → item id, so other tooling need not rescan 193 jars. |
| `dev/scripts/generators/apply_ftbquests_chapter_icons.py` | the only writer of chapter icons. Idempotent; `--check` for dry run. |
| `dev/scripts/audit_ftbquests_chapter_icons.py` | validator. Hard-fails the string form. |
| `dev/scripts/generators/ensure_ftbquest_icons.js` | owns **quest** icons only, in compound form. Validates chapter icons against the lockfile; no longer rewrites them. |

All 45 chapters now carry a fixed compound icon. The Era 1–8 chapters carry 371
explicit compound quest icons.

Era icon choices are the ones that were already established in
`ensure_ftbquest_icons.js` (`create:andesite_alloy`, `tfmg:steel_ingot`,
`petrochem:distillation_controller`, `powergrid:integrated_circuit`,
`oritech:machine_core_4`, `create_new_age:reactor_rod`, `stellaris:rocket`,
`kubejs:infinite_domain_core`); all eight resolve.

## Rules

1. **Never write `icon: "<id>"`.** Always `icon: { id: "<id>" }`. Any tool that
   emits the string form is a regression, however "deterministic" it claims to be.
2. Chapter icons belong to the Python generator. Nothing else writes them.
3. An icon id must exist, or it renders as `ftbquests:missing_item`.
   `kubejs:`-namespace ids are registered at runtime from template literals and
   cannot be verified statically — the audit reports those as *unverified* rather
   than failing.
4. Run the audit after anything touches `config/ftbquests/quests/chapters/`.

## Not yet verified

The icons are correct on disk and survive the documented load/save path by
construction. **They have not been seen in a running client.** The remaining check
is to open the quest book, confirm each chapter button shows one static icon, then
quit and confirm `git diff` on `config/ftbquests/quests/chapters/` is empty — that
last step is the one that has always failed before.
