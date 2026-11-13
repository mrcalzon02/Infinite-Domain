# Infinite Domain — Pre-development benchmark checkpoint (2026-11-13)

**Checkpoint ID:** `ID-BENCH-2026-11-13-f1ee5203`  
**Audited source commit (`main`, before this report):** `f1ee52034dde50a1ea8ca1352c9a28e2804ecfef`  
**Purpose:** Preserve a reproducible progress baseline before the next development iteration.  
**Classification:** **Source-inventory and retained-evidence audit; NOT a newly built or published release, NOT a fresh runtime test.**

## Scope and method

The checkpoint was reconciled directly against the live repository's `main` branch and the committed source/validation outputs on 2026-11-13. Thirteen consistency assertions passed on the manifest, owned-JAR inventory, script inventory, retained runtime results, log category totals, static geography reports, structure corpus, production approvals, gate statuses, and QA-gallery state. This was a **readback/data-consistency check**, not re-execution of the project scripts or a Minecraft process.

- Game: **Minecraft 1.21.1**; loader: **NeoForge 21.1.248** (`minecraftinstance.json`).
- CurseForge metadata: **184 installed-add-on entries**. Third-party mods are intentionally *not* included in this repository; reconstruct from authorized original distribution channels according to `dev/REPOSITORY_SCOPE.md`.
- Project-owned `mods/infinite-domain-*.jar` files present: **11**, including `infinite-domain-boot-data-compat-1.0.0.jar`. The source area includes `dev/packdev/` and `packdev/overworld-terrain-companion/`.
- KubeJS source inventory: **14 startup scripts, 25 server scripts**.
- The older `dev/PROJECT_INDEX.md` enumeration of **10** project JARs predates the boot-data compatibility JAR; use the current live inventory for this checkpoint.
- GitHub Releases list: **no published releases** at audit time. The latest listed GitHub Actions run is 2026-08-26, predating the audited source commit. Neither constitutes build validation for this SHA.

## Retained runtime baseline — 2026-10-14

**Run:** `20261014-dimension-repair-r4-r01`  
**Evidence:** `dev/docs/boot-dimension-audit/revision-4/{README.md,result.json,log-summary.json,live-acceptance.json}`.

- Isolated NeoForge dedicated server: **completed**; fresh fixed-seed dimension-audit suite: **64 / 64 chunks**, four 4×4 tiles (Overworld, Nether, Hive arrival, Hive remote).
- Acceptance-probe errors: **0**. Lost Cities, Dungeons Arise, and Seven Seas were loaded; natural structure starts observed in the four limited tiles: **0**. No natural structure frequency or visual-quality conclusion follows from that small sample.
- KubeJS at that run: **14/14 startup** and **25/25 server** scripts loaded with no script load errors.
- Remaining **10 ERROR lines**: **7** invalid `minecraft:mob_spawner` block entities at air, **2** Stellaris recipe-scanner errors, **1** Moonlight compatibility advisory. The 7 spawner errors are **not repaired or definitively attributed**.
- Separately retained: **5** Windows invalid-path exceptions. No claim of an error-free startup.
- Timing: **`measurementQuality: unmeasured`**, with all four tiles accepted on their first poll. Any `chunksPerSecond`, p95 or apparent speedup from this run is **not a defensible throughput measurement**. Use the defined standard suite with repeated measurable tiles for performance comparison.
- This run is **historical evidence**, not a fresh launch against the audited source commit, and does not establish a client launch, real player travel, new-world natural landmark reachability, or multiplayer acceptance.

## Source-only follow-up after the runtime

The 2026-10-28/29 commits introduced and tested first-party spawner error provenance and placement-event evidence validation. The retained revision-4 errors form **three spatial groups of sizes 2, 1 and 4**, not known structure IDs. The placement validator checks run-ID isolation, source ownership, rotation/mirror transforms, negative chunk coordinates and observed state/NBT fields. **No upstream natural-placement interception hook has yet produced first-party live placement evidence.** The exact owner of the 7 errors remains unknown.

References: `dev/scripts/audit_spawner_runtime_provenance.py`, `dev/scripts/audit_spawner_placement_events.py`, their `test_*.py` modules, and `dev/docs/boot-dimension-audit/revision-4/README.md`.

## Static evidence inventory (retained; not rerun here)

| Area | Retained evidence | Interpretation |
| --- | --- | --- |
| Overworld geography | `dev/docs/overworld-geography-validation.json`: **13/13 checks passing** | Source topology/ownership, not fresh-client appearance |
| Wasteland hex caves | `dev/docs/wasteland-hex-cave-validation.json`: **13/13 checks passing** | Geometry/codec/registration contract; new-seed visual + performance checks remain |
| Structure corpus | `dev/docs/structure-corpus-validation.json`: **184 records, valid** | Structural metadata/source integrity; not visual approval |
| Production structures | `dev/docs/production-integration-validation.json`: **36 approved of 85 checked**, 8 settlement archetypes active, zero reported validation failures | Candidate production progress, not proof of natural spawning in the world |
| Structure pipeline | `dev/docs/structure-pipeline-completion-audit.json`: **7 of 15 gates achieved**, 8 remaining; completion marker disallowed | Active development |
| Structure QA gallery | `dev/docs/structure-qa-world-validation.json`: **94** structures, **84** road modules, **21** reusable kit modules; static integrity passed | `structure-runtime-review.json` still records runtime review incomplete |
| Launcher archive audit | `dev/docs/worldgen-benchmark/launcher-validation.json`: retained pass | Historical installer/library checks; explicitly **not a new server launch** |

## Release / benchmark decision

This is an **immutable source-SHA checkpoint**, suitable for measuring progress before the next development pass. **No release asset, signed manifest, Git tag, published prerelease, or current-SHA runnable build is claimed.** The GitHub documentation commit that records this checkpoint does not change the audited runtime content.

Do **not** treat unfinished visual, balance or style tasks as automatic release blockers. For a distributable benchmark, apply the project's release-blocking threshold to **build/launch/run failures and required multiplayer/updater failures**. The 10 nonfatal log errors remain important diagnostics; investigate their actual effects without misrepresenting a completed smoke run as clean. A usable benchmark archive still requires a reproducible build and fresh runtime proof.

## Required next evidence before advertising a runnable benchmark

1. Reconstruct the authorized full CurseForge instance on a capable local runner; verify Java 21 and pinned NeoForge 21.1.248. Do not ship third-party JARs or uncleared resource-pack content.
2. Build and fingerprint the **11 owned JARs** and run relevant source checks. The currently checked-in JARs are inventory evidence, not newly rebuilt outputs.
3. From a complete **instance** layout, rerun the project's existing `scripts/run_worldgen_benchmark.ps1` with `-Variant baseline -Suite dimension_audit -Repetitions 1 -KeepRuntime`. Keep `result.json`, log summary, complete log, build checksums and exact source SHA. Recheck actual launch, 64/64 completion and acceptance-probe results.
4. Run the actual client and required multiplayer journey/reconnect checks before marking those paths certified. Nether/Hive portal travel, natural structures, and gallery visuals remain unverified; visual-quality assessment is diagnostic rather than an automatic release gate.
5. For a **performance** benchmark, run an interleaved, repeatable baseline/variant series on the **standard** suite, at least three repetitions where measurement quality is `measured`. Do not compare first-poll-saturated timings.
6. Only then create an actual prerelease/tag and attach a packaged, redistribution-compliant artifact with checksums. Preserve this checkpoint's original `f1ee5203` source identity for future comparisons; do not reassign a moving tag.

**Sources:** Live `main` branch and paths above, read 2026-11-13. Unverified claims are deliberately left unverified.
