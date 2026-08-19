# Era 0 Quest Design — Lost Survivors

Era 0 teaches the player that survival and infrastructure are collective processes. Charles, an extradimensional intelligence who witnessed the world's collapse, narrates the guide. He offers limited emergency supplies but primarily provides analysis, lost knowledge, and procedural direction.

## Implemented three-path sequence

1. Read Charles's opening transmission and understand the pack's collaborative premise.
2. Establish shelter in the central wasteland.
3. Learn that dead bushes and ferns provide sticks, seeds, compostable vegetation, and sparse scrap.
4. Recover bones from the dead and craft Primitive Start bone tools.
5. Consolidate Wastelands scrap into processable Scrap Piles.
6. Build an Ex Deorum hammer, String Mesh, and first sieve.
7. Learn the mesh-dependent and deliberately sparse salvage process.
8. Introduce AllTheCompressed as the pack's infrastructure accounting system.
9. Accumulate eight 3x Compressed Cobblestone and construct the first furnace.

The chapter now contains three ordered profession paths: Ruin Scavenger, Bone/Stone/Fire, and Habitation/Sustenance. Each ends in a crafted contribution item. Completing any one endpoint unlocks the convergence quest; the other paths remain available for rewards and settlement development.

The furnace is explicitly presented as a communal milestone. Every valid route consumes eight 3x Compressed Cobblestone, representing 5,832 ordinary cobblestone, plus one profession contribution in the center. This makes the furnace the first task whose sensible solution is organized division of labor.

Small Numismatics payments appear between milestones. They establish the Survivor Exchange economy without replacing material progression.

## Starting guide

`kubejs/server_scripts/main.js` gives every player one `ftbquests:book` the first time they log in after this system is installed. A persistent player flag prevents reconnects and deaths from duplicating the book.
