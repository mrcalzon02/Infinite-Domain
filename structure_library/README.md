# Infinite Domain Structure Corpus

This is the source-of-truth library for buildings admitted to the Lost Cities replacement pipeline. Production world generation must reference approved derivatives, never an unreviewed rough source directly.

Lifecycle:

1. `rough_source` — imported or existing recognizable geometry.
2. `clean_master` — heavily rebuilt, architecturally articulated, fully programmed building without wasteland damage.
3. `damage_variant` — spatially coherent damage derived from the clean master.
4. `occupation_variant` — gameplay state layered onto a clean or damaged derivative.
5. `approved` — automatic validation and visual review both complete.

The bungalow heavy rebuild is the minimum standard for every algorithmically generated structure. Each type must now declare its building program and circulation, preserve an immutable clean master, pass structure-specific logistical checks, and receive four rendered review views before any damage derivative is considered.

The corpus is deliberately mixed and includes rough sources plus clean masters. Every entry remains quarantined from the Lost Cities building selectors until its clean master, conversion, rendered review, in-world walk-through and human approval are complete. The enforceable sequence and minimum detail requirements are recorded in `generated-structure-refinement-policy.json`.
