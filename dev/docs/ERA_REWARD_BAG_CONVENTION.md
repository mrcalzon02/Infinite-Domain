# Era Reward Bag Convention

Date: 2026-08-14

Era reward bags are small randomized acknowledgements for optional side work and
educational quests. They make lessons feel materially useful without replacing
the deliberate recipes, machines, or capstones those lessons explain.

## Tiers

Era 0 retains the existing Garbage Bag as its common reward. It is processed
through the established sieve system rather than opened directly. A Sealed
Survival Cache provides the Era 0 rare counterpart.

Eras 1–8 each have two non-craftable KubeJS items:

- a common Supply Bag, making two independent weighted rolls;
- a glowing rare Priority Cache, making four independent weighted rolls.

All new bags open by right-clicking in the air and consume exactly one bag. They
stack to 64. Bags are not stage-locked internally: access is controlled by which
quests and systems award the correct era's item.

## Reward design

| Era | Common identity | Rare identity |
|---:|---|---|
| 0 | Garbage Bag: basic salvage, food, and filtration | concentrated survival supplies and a very rare Gas Mask |
| 1 | shafts, cogwheels, belts, Andesite Alloy, rope | Precision Mechanisms, brass parts, sturdy sheets, storage upgrades |
| 2 | steelmaking feedstock, coke, refractory blocks, pipes | steel mechanisms, casings, tanks, pumps, reinforced refractory parts |
| 3 | plastics, rubber, sulfur, coke, pipes, engine parts | circuits, fluid tanks, pumpjack parts, chemical intermediates |
| 4 | wires, coils, circuit boards, magnets, connectors | integrated circuits, transformers, batteries, motors, generator coils |
| 5 | quartz, Fluix parts, basic processors, motors, cyber components | advanced processors, cell components, machine cores, specialist cyber components |
| 6 | fuel-cycle materials, shielding supplies, medicine | enriched fuel, rods, reactor casing, advanced batteries, Plutonium |
| 7 | orbital metals, oxygen storage, ice, advanced cores | material blocks, habitat oxygen, high-capacity cells and batteries |
| 8 | superconductors, Prometheum, advanced processors and materials | 256k components, tier-seven cores, dense power, endgame feedstock |

Complete gateway machines, controllers, reactors, rockets, capstones, Foundation
Cores, and Infinite Domain items are excluded. A lesson about constructing a
machine may reward useful replacement parts, but never the completed machine.

## Quest placement

`scripts/generators/assign_era_reward_bags.py` examines gear-shaped technical lessons in
each era chapter. It leaves quests with bespoke rewards alone, assigns a common
bag to approximately every third eligible lesson plus specifically designated
core tutorials, and assigns the last eligible technical lesson a rare cache. The
Era 3 Refinery Output Bank is the first designated multiblock lesson. The process
is deterministic and idempotent.

The exact placements are indexed in
`docs/era-reward-bags/reward-assignments.csv`. Future quest writing should follow
the same convention:

- one common bag for a short practical lesson or small side objective;
- one rare cache for a multi-step lesson, dangerous optional exercise, or the
  end of a coherent educational subsection;
- no bag for routine item hand-ins, required capstones, or quests already carrying
  a deliberately authored unique reward;
- never award a bag from an era later than the quest that grants it.
