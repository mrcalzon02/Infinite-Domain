# Gateway of Doom Configuration

Date: 2026-08-14

Gateway of Doom 2.1.0 remains installed for deliberate encounters. Its passive
scheduler is enabled only for ordinary Cyberspace in
`config/gateway_of_doom.json`:

- `automaticGateways.enabled` is `true`;
- `overworld_exploration.enabled` is `false`;
- `nether_timer.enabled` is `false`;
- `end_timer.enabled` is `false`.
- `cyberspace_timer.enabled` is `true` and targets only
  `cyberspace:cyberspace_dimension`.

The Cyberspace rule uses the hard profile, waits 30–60 minutes between attempts,
requires at least one player, permits one active gateway, and places it 48–128
blocks from the selected player. The Darknet is deliberately excluded because
its timed session, Mekanites, and dragons already provide its encounter pressure.

This prevents random Gateway waves in the Overworld, Nether, End, and Darknet.
`kubejs/server_scripts/gateway_of_doom_dimension_lock.js` also cancels manual use
of every Devil Eye outside ordinary Cyberspace. This includes the Overworld,
Nether, End, Darknet, and modded dimensions. Portal Wards, configured profiles,
administrative commands, and quest/script activations remain available, but a
player can only activate an Eye in `cyberspace:cyberspace_dimension`.
Rejected activation attempts do not consume the Eye. Charles selects one of
eight mildly condescending responses, each beginning with the unambiguous
warning `This is only usable in Cyberspace.` The response identifies the
player's current dimension, with normalized names for the Overworld, Nether,
End, and Darknet. The complete response remains in chat, while a concise title
and dimension-specific subtitle remain on screen for 75 seconds.

## Cyberware recipe integration

All five Portal Ward recipes are overridden in
`kubejs/data/gateway_of_doom/recipe/`. Every tier consumes Cyberware Port parts,
and tiers II–V also consume the preceding Ward:

1. Component Box, Fiber Optics, Microelectronics, and Crying Obsidian;
2. Fiber Optics, Plating, Storage, and Portal Ward I;
3. Microelectronics, Reactor Components, Titanium Components, and Portal Ward II;
4. Fullerene Components, Solid-State Cells, Dense Batteries, and Portal Ward III;
5. Reactor Components, a Matrix, Consciousness Transmitters, and Portal Ward IV.

Gateway of Doom does not provide crafting recipes for its Devil Eyes. The pack
adds a deliberate three-step encounter progression:

1. **Devil Eye (Easy):** Data Hardware, Portal Ward I, Fiber Optics, and
   Microelectronics;
2. **Devil Eye (Medium):** a Virtual Machine Core, Portal Ward II, Titanium,
   Reactor Components, Storage, and Microelectronics;
3. **Devil Eye (Hard):** a Quantum Core, Portal Ward III, Fiber Optics, Reactor
   Components, Microelectronics, and a Matrix.

The fixed variants reliably select their intended encounter profiles. The bare
Devil Eye remains uncraftable because a plain stack lacks explicit profile data.
No Gateway item is used to craft a Cyberware or Cyberspace component, so the
integration is non-circular.
